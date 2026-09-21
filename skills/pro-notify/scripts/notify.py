#!/usr/bin/env python3
"""Explicit, text-only notifications. Credentials never appear in CLI output."""

import argparse
import base64
from contextlib import contextmanager
import hashlib
import hmac
import json
import math
import os
from pathlib import Path
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid


HOME = Path.home() / ".config" / "pro-notify"
PROVIDERS = ("feishu", "dingtalk", "wecom")
EVENTS = ("manual", "completed", "failed", "needs-input")
SERVICE = "pro-notify"
DEDUP_SECONDS = 86400
NAME = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}\Z")
ENV_NAME = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*\Z")


class NotifyError(Exception):
    """Only fixed, safe error codes belong in this exception."""


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        # Invalid arguments may themselves contain a mistakenly pasted credential.
        self.exit(2, '{"status": "error", "error": "invalid_arguments"}\n')


def read_json(path, default=None):
    try:
        with Path(path).open(encoding="utf-8-sig") as handle:
            return json.load(handle)
    except FileNotFoundError:
        if default is not None:
            return default
        raise NotifyError("config_missing") from None
    except (OSError, ValueError):
        raise NotifyError("json_read_failed") from None


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".notify-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


@contextmanager
def locked(path):
    path = Path(path)
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    lock = path.with_name(path.name + ".lock")
    deadline = time.monotonic() + 3
    while True:
        try:
            fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            os.close(fd)
            break
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise NotifyError("state_locked") from None
            time.sleep(0.05)
    try:
        yield
    finally:
        lock.unlink()


def secure_keyring():
    try:
        import keyring
        backend = keyring.get_keyring()
        candidates = getattr(backend, "backends", [backend])
        allowed = {
            "keyring.backends.Windows",
            "keyring.backends.macOS",
            "keyring.backends.SecretService",
            "keyring.backends.kwallet",
        }
        for candidate in candidates:
            if type(candidate).__module__ in allowed and candidate.priority > 0:
                return candidate
    except Exception:
        raise NotifyError("keyring_unavailable") from None
    raise NotifyError("secure_keyring_required")


def env_value(name):
    if not isinstance(name, str) or not ENV_NAME.fullmatch(name):
        raise NotifyError("invalid_env_reference")
    value = os.environ.get(name)
    if not value:
        raise NotifyError("credential_missing")
    return value


def resolve(ref):
    if not isinstance(ref, dict) or len(ref) != 1:
        raise NotifyError("invalid_credential_reference")
    if "env" in ref:
        return env_value(ref["env"])
    if "keyring" in ref and isinstance(ref["keyring"], str):
        try:
            value = secure_keyring().get_password(SERVICE, ref["keyring"])
        except Exception:
            raise NotifyError("keyring_read_failed") from None
        if isinstance(value, str) and value:
            return value
        raise NotifyError("credential_missing")
    raise NotifyError("invalid_credential_reference")


def validate_url(provider, url):
    try:
        parts = urllib.parse.urlsplit(url)
        if (
            parts.scheme != "https" or parts.port not in (None, 443)
            or parts.username is not None or parts.password is not None
            or parts.fragment or any(c.isspace() or ord(c) < 32 for c in url)
        ):
            raise ValueError
        query = urllib.parse.parse_qs(parts.query, keep_blank_values=True)
        if provider == "feishu":
            valid = (
                parts.hostname in ("open.feishu.cn", "open.larksuite.com")
                and re.fullmatch(r"/open-apis/bot/v2/hook/[A-Za-z0-9_-]+", parts.path)
                and not parts.query
            )
        elif provider in ("dingtalk", "wecom"):
            host, path, field = {
                "dingtalk": ("oapi.dingtalk.com", "/robot/send", "access_token"),
                "wecom": ("qyapi.weixin.qq.com", "/cgi-bin/webhook/send", "key"),
            }[provider]
            valid = (
                parts.hostname == host and parts.path == path
                and set(query) == {field} and len(query[field]) == 1
                and bool(query[field][0])
            )
        else:
            valid = False
        if not valid:
            raise ValueError
    except (ValueError, TypeError, AttributeError):
        raise NotifyError("invalid_webhook_url") from None


def load_config(path, missing_ok=False):
    data = read_json(path, {"version": 1, "channels": {}} if missing_ok else None)
    if (
        not isinstance(data, dict) or type(data.get("version")) is not int
        or data["version"] != 1 or not isinstance(data.get("channels"), dict)
    ):
        raise NotifyError("invalid_config")
    for name, channel in data["channels"].items():
        if (
            not NAME.fullmatch(name) or not isinstance(channel, dict)
            or channel.get("provider") not in PROVIDERS
            or set(channel) - {"provider", "webhook", "signing_secret"}
            or "webhook" not in channel
        ):
            raise NotifyError("invalid_channel")
        if channel["provider"] == "wecom" and "signing_secret" in channel:
            raise NotifyError("wecom_does_not_use_signing_secret")
        for field in ("webhook", "signing_secret"):
            if field not in channel:
                continue
            ref = channel[field]
            if (
                not isinstance(ref, dict) or len(ref) != 1
                or not set(ref) <= {"env", "keyring"}
                or not isinstance(next(iter(ref.values())), str)
            ):
                raise NotifyError("invalid_credential_reference")
    return data


def configure(name, provider, webhook_env, signing_secret_env=None,
              store="keyring", replace=False, config_path=None):
    """Persist references, optionally copying process env values to the OS vault."""
    path = Path(config_path) if config_path else HOME / "config.json"
    if not isinstance(name, str) or not NAME.fullmatch(name) or provider not in PROVIDERS:
        raise NotifyError("invalid_channel")
    if store not in ("env", "keyring"):
        raise NotifyError("invalid_store")
    if provider == "wecom" and signing_secret_env:
        raise NotifyError("wecom_does_not_use_signing_secret")
    values = {"webhook": env_value(webhook_env)}
    validate_url(provider, values["webhook"])
    refs = {"webhook": {"env": webhook_env}}
    if signing_secret_env:
        values["signing_secret"] = env_value(signing_secret_env)
        refs["signing_secret"] = {"env": signing_secret_env}
    with locked(path):
        data = load_config(path, missing_ok=True)
        if name in data["channels"] and not replace:
            raise NotifyError("channel_exists_use_replace")
        backend = secure_keyring() if store == "keyring" else None
        created = []
        try:
            if backend:
                for field, value in values.items():
                    account = f"{name}/{field}/{uuid.uuid4().hex}"
                    backend.set_password(SERVICE, account, value)
                    created.append(account)
                    refs[field] = {"keyring": account}
            data["channels"][name] = {"provider": provider, **refs}
            write_json(path, data)
        except Exception:
            for account in created:
                try:
                    backend.delete_password(SERVICE, account)
                except Exception:
                    pass
            raise NotifyError("configuration_write_failed") from None
    return {"channel": name, "provider": provider, "status": "configured", "store": store}


def build_request(channel, text, now=None):
    provider = channel["provider"]
    url = resolve(channel["webhook"])
    validate_url(provider, url)
    parts = urllib.parse.urlsplit(url)
    destination = (parts.path if provider == "feishu"
                   else urllib.parse.parse_qs(parts.query)[
                       "key" if provider == "wecom" else "access_token"
                   ][0])
    endpoint_id = hashlib.sha256(
        json.dumps([parts.hostname, destination]).encode()
    ).hexdigest()
    now = time.time() if now is None else now
    if provider == "feishu":
        payload = {"msg_type": "text", "content": {"text": text}}
    else:
        payload = {"msgtype": "text", "text": {"content": text}}
    if "signing_secret" in channel:
        secret = resolve(channel["signing_secret"])
        if provider == "feishu":
            stamp = str(int(now))
            digest = hmac.new(f"{stamp}\n{secret}".encode(), b"", hashlib.sha256).digest()
            payload.update(timestamp=stamp, sign=base64.b64encode(digest).decode())
        elif provider == "dingtalk":
            stamp = str(int(now * 1000))
            digest = hmac.new(
                secret.encode(), f"{stamp}\n{secret}".encode(), hashlib.sha256
            ).digest()
            url += "&" + urllib.parse.urlencode({
                "timestamp": stamp, "sign": base64.b64encode(digest).decode()
            })
    # Hash the destination, not the signature or alias, for shared rate limits.
    return provider, url, payload, endpoint_id


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def post(provider, url, payload):
    request = urllib.request.Request(
        url, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        opener = urllib.request.build_opener(NoRedirect())
        with opener.open(request, timeout=10) as response:
            if not 200 <= response.status < 300:
                raise NotifyError("http_rejected")
            raw = response.read(65537)
            if len(raw) > 65536:
                raise NotifyError("response_unconfirmed")
        result = json.loads(raw)
        if not isinstance(result, dict):
            raise NotifyError("response_unconfirmed")
        field = "code" if provider == "feishu" else "errcode"
        if provider == "feishu" and field not in result:
            field = "StatusCode"
        code = result.get(field)
        if type(code) is not int:
            raise NotifyError("response_unconfirmed")
        if code != 0:
            raise NotifyError("provider_rejected")
    except urllib.error.HTTPError as exc:
        error = "http_rate_limited" if exc.code == 429 else "http_rejected"
        exc.close()
        raise NotifyError(error) from None
    except (urllib.error.URLError, OSError, TimeoutError):
        raise NotifyError("delivery_unconfirmed") from None
    except (ValueError, UnicodeError):
        raise NotifyError("response_unconfirmed") from None


def valid_state(data):
    if not isinstance(data, dict) or set(data) != {"attempts", "events"}:
        raise NotifyError("invalid_state")
    if not isinstance(data["attempts"], dict) or not isinstance(data["events"], dict):
        raise NotifyError("invalid_state")
    for times in data["attempts"].values():
        if not isinstance(times, list) or any(
            type(t) not in (int, float) or not math.isfinite(t) or t < 0 for t in times
        ):
            raise NotifyError("invalid_state")
    for entry in data["events"].values():
        if (
            not isinstance(entry, dict) or type(entry.get("time")) not in (int, float)
            or not math.isfinite(entry["time"]) or entry["time"] < 0
            or entry.get("status") not in ("reserved", "accepted", "failed", "unconfirmed")
        ):
            raise NotifyError("invalid_state")
    return data


def reserve(path, endpoint_id, event_id, now):
    with locked(path):
        data = valid_state(read_json(path, {"attempts": {}, "events": {}}))
        data["attempts"] = {
            key: [stamp for stamp in stamps if now - stamp < 60]
            for key, stamps in data["attempts"].items()
            if any(now - stamp < 60 for stamp in stamps)
        }
        data["events"] = {
            key: entry for key, entry in data["events"].items()
            if now - entry["time"] < DEDUP_SECONDS
        }
        if event_id and event_id in data["events"]:
            return {"status": "duplicate", "previous_status": data["events"][event_id]["status"]}
        stamps = data["attempts"].setdefault(endpoint_id, [])
        if len(stamps) >= 20:
            return {"status": "rate_limited"}
        stamps.append(now)
        if event_id:
            data["events"][event_id] = {"time": now, "status": "reserved"}
        write_json(path, data)
    return None


def finish(path, event_id, status):
    if not event_id:
        return
    with locked(path):
        data = valid_state(read_json(path))
        data["events"][event_id]["status"] = status
        write_json(path, data)


def send(channels, text, event="manual", task_id=None, dry_run=False,
         config_path=None, state_path=None):
    """Send only to selected aliases; the caller must already have user authorization."""
    if not isinstance(text, str) or not text.strip() or len(text.encode("utf-8")) > 2048:
        raise NotifyError("text_required_max_2048_bytes")
    if event not in EVENTS or (event != "manual" and (not isinstance(task_id, str) or not task_id.strip())):
        raise NotifyError("event_requires_task_id")
    if not isinstance(channels, (list, tuple)) or not channels:
        raise NotifyError("select_channels")
    data = load_config(config_path or HOME / "config.json")
    selected = list(dict.fromkeys(channels))
    if any(name not in data["channels"] for name in selected):
        raise NotifyError("channel_not_found")
    # Preflight all destinations before any outward action.
    plans = [(name, build_request(data["channels"][name], text)) for name in selected]
    results = []
    path = Path(state_path) if state_path else HOME / "state.json"
    for name, (provider, url, payload, endpoint_id) in plans:
        result = {"channel": name, "provider": provider}
        if dry_run:
            results.append({**result, "status": "dry_run"})
            continue
        event_id = None
        if event != "manual":
            event_id = hashlib.sha256(
                json.dumps([endpoint_id, task_id, event], ensure_ascii=False).encode()
            ).hexdigest()
        try:
            blocked = reserve(path, endpoint_id, event_id, time.time())
            if blocked:
                results.append({**result, **blocked})
                continue
        except (NotifyError, OSError):
            results.append({**result, "status": "failed", "error": "state_unavailable"})
            continue
        try:
            post(provider, url, payload)
            result["status"] = "accepted"
        except NotifyError as exc:
            result.update(
                status="unconfirmed" if str(exc).endswith("unconfirmed") else "failed",
                error=str(exc),
            )
        except Exception:
            result.update(status="unconfirmed", error="delivery_unconfirmed")
        try:
            finish(path, event_id, result["status"])
        except (NotifyError, OSError):
            # Preserve the delivery result; never retry just because bookkeeping failed.
            result["state_warning"] = "state_update_failed"
        results.append(result)
    return results


def main(argv=None):
    parser = SafeParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=HOME / "config.json")
    commands = parser.add_subparsers(dest="command", required=True)
    setup = commands.add_parser("configure", help="Configure using named process environment values")
    setup.add_argument("--name", required=True)
    setup.add_argument("--provider", choices=PROVIDERS, required=True)
    setup.add_argument("--webhook-env", required=True)
    setup.add_argument("--signing-secret-env")
    setup.add_argument("--store", choices=("keyring", "env"), default="keyring")
    setup.add_argument("--replace", action="store_true")
    commands.add_parser("list", help="List aliases, never credentials")
    notify = commands.add_parser("send", help="Send an explicitly authorized plain-text message")
    notify.add_argument("--channel", action="append", required=True)
    source = notify.add_mutually_exclusive_group(required=True)
    source.add_argument("--message-stdin", action="store_true")
    source.add_argument("--message-file", type=Path)
    notify.add_argument("--event", choices=EVENTS, default="manual")
    notify.add_argument("--task-id")
    notify.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "configure":
            output = configure(
                args.name, args.provider, args.webhook_env, args.signing_secret_env,
                args.store, args.replace, args.config,
            )
        elif args.command == "list":
            config = load_config(args.config)
            output = [{"channel": name, "provider": channel["provider"]}
                      for name, channel in config["channels"].items()]
        else:
            import sys
            text = (sys.stdin.read() if args.message_stdin
                    else args.message_file.read_text(encoding="utf-8-sig"))
            output = send(args.channel, text, args.event, args.task_id,
                          args.dry_run, args.config)
        print(json.dumps(output, ensure_ascii=True))
        if args.command == "send":
            return int(any(
                (item["status"] not in ("accepted", "dry_run", "duplicate"))
                or (item["status"] == "duplicate" and item["previous_status"] != "accepted")
                or "state_warning" in item for item in output
            ))
        return 0
    except NotifyError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}))
        return 1
    except Exception:
        # Exception messages can contain credentialed URLs, response bodies or file data.
        print(json.dumps({"status": "error", "error": "operation_failed"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

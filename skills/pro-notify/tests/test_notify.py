"""Offline contract tests. All HTTP and OS vault operations are mocked."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr, redirect_stdout
import base64
import hashlib
import hmac
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
import urllib.error
import urllib.parse


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "notify.py"
SPEC = importlib.util.spec_from_file_location("pro_notify", SCRIPT)
notify = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(notify)

# Deliberately fictitious values, never usable credentials.
URLS = {
    "wecom": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=unit-test-only",
    "feishu": "https://open.feishu.cn/open-apis/bot/v2/hook/unit-test-only",
    "dingtalk": "https://oapi.dingtalk.com/robot/send?access_token=unit-test-only",
}


class NotifyTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.home = Path(self.directory.name)
        self.config = self.home / "config.json"
        self.state = self.home / "state.json"
        self.home_patch = patch.object(notify, "HOME", self.home)
        self.home_patch.start()
        self.addCleanup(self.home_patch.stop)
        self.env_patch = patch.dict(os.environ, {
            "TEST_WECOM": URLS["wecom"],
            "TEST_FEISHU": URLS["feishu"],
            "TEST_DINGTALK": URLS["dingtalk"],
            "TEST_SIGN": "unit-test-signing-value",
        })
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)
        # Any accidental attempt to use the real network fails immediately.
        self.network_patch = patch.object(
            notify.urllib.request, "build_opener", side_effect=AssertionError("network_forbidden")
        )
        self.network_patch.start()
        self.addCleanup(self.network_patch.stop)
        self.vault_patch = patch.object(
            notify, "secure_keyring", side_effect=AssertionError("vault_forbidden")
        )
        self.vault_patch.start()
        self.addCleanup(self.vault_patch.stop)

    def configure(self, name="work", provider="wecom", **kwargs):
        return notify.configure(name, provider, f"TEST_{provider.upper()}",
                                store="env", config_path=self.config, **kwargs)

    def send(self, text="任务已完成", channels=None, **kwargs):
        return notify.send(channels or ["work"], text, config_path=self.config,
                           state_path=self.state, **kwargs)

    def cli(self, *args, text="通知"):
        output = io.StringIO()
        with redirect_stdout(output), patch("sys.stdin", io.StringIO(text)):
            code = notify.main(["--config", str(self.config), *args])
        return code, json.loads(output.getvalue())

    def response(self, body, status=200):
        response = Mock(status=status)
        response.read.return_value = body
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        opener = Mock()
        opener.open.return_value = response
        return opener

    def test_configure_env_stores_only_reference(self):
        result = self.configure()
        contents = self.config.read_text(encoding="utf-8")
        self.assertNotIn(URLS["wecom"], contents)
        self.assertEqual(result["store"], "env")
        self.assertEqual(notify.load_config(self.config)["channels"]["work"]["webhook"],
                         {"env": "TEST_WECOM"})
        self.assertFalse(self.state.exists())

    def test_keyring_persists_and_is_reused_without_original_env(self):
        vault = {}
        backend = Mock()
        backend.set_password.side_effect = lambda service, name, value: vault.update({name: value})
        backend.get_password.side_effect = lambda service, name: vault.get(name)
        with patch.object(notify, "secure_keyring", return_value=backend):
            notify.configure("work", "wecom", "TEST_WECOM", config_path=self.config)
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(self.send(dry_run=True)[0]["status"], "dry_run")
        self.assertEqual(list(vault.values()), [URLS["wecom"]])
        self.assertNotIn(URLS["wecom"], self.config.read_text(encoding="utf-8"))

    def test_keyring_failure_never_falls_back_to_plaintext(self):
        with patch.object(notify, "secure_keyring", side_effect=notify.NotifyError("keyring_unavailable")):
            with self.assertRaisesRegex(notify.NotifyError, "keyring_unavailable"):
                notify.configure("work", "wecom", "TEST_WECOM", config_path=self.config)
        self.assertFalse(self.config.exists())

    def test_secure_backend_rejects_untrusted_file_backend(self):
        self.vault_patch.stop()
        backend = Mock(priority=1)
        fake = Mock()
        fake.get_keyring.return_value = backend
        backend.backends = [backend]
        with patch.dict(sys.modules, {"keyring": fake}):
            with self.assertRaisesRegex(notify.NotifyError, "secure_keyring_required"):
                notify.secure_keyring()

    def test_secure_backend_selects_native_from_chainer(self):
        self.vault_patch.stop()
        native = type("Native", (), {"__module__": "keyring.backends.Windows", "priority": 5})()
        fake = Mock()
        fake.get_keyring.return_value = type("Chain", (), {"backends": [Mock(), native]})()
        with patch.dict(sys.modules, {"keyring": fake}):
            self.assertIs(notify.secure_keyring(), native)

    def test_failed_config_write_rolls_back_new_vault_entries(self):
        backend = Mock()
        with patch.object(notify, "secure_keyring", return_value=backend):
            with patch.object(notify, "write_json", side_effect=OSError("synthetic")):
                with self.assertRaisesRegex(notify.NotifyError, "configuration_write_failed"):
                    notify.configure("work", "wecom", "TEST_WECOM", config_path=self.config)
        backend.delete_password.assert_called_once()
        self.assertFalse(self.config.exists())

    def test_replace_is_explicit_and_preserves_other_channels(self):
        self.configure()
        self.configure("alerts", "feishu")
        original = self.config.read_bytes()
        with self.assertRaisesRegex(notify.NotifyError, "channel_exists_use_replace"):
            self.configure(provider="dingtalk")
        self.assertEqual(self.config.read_bytes(), original)
        self.configure(provider="dingtalk", replace=True)
        config = notify.load_config(self.config)
        self.assertEqual(set(config["channels"]), {"work", "alerts"})
        self.assertEqual(config["channels"]["work"]["provider"], "dingtalk")

    def test_invalid_channel_and_missing_env_are_safe(self):
        for name in ("../escape", "line\nbreak", "", "a" * 65):
            with self.subTest(name=name), self.assertRaises(notify.NotifyError):
                self.configure(name=name)
        with self.assertRaisesRegex(notify.NotifyError, "credential_missing"):
            notify.configure("work", "wecom", "NONEXISTENT_NOTIFY_TEST", store="env",
                             config_path=self.config)
        self.assertFalse(self.config.exists())

    def test_wecom_rejects_signing_config(self):
        with self.assertRaisesRegex(notify.NotifyError, "wecom_does_not"):
            self.configure(signing_secret_env="TEST_SIGN")

    def test_malformed_config_and_inline_credentials_are_rejected(self):
        for value in ([], {"version": True, "channels": {}},
                      {"version": 1, "channels": {"work": {
                          "provider": "wecom", "webhook": URLS["wecom"]}}}):
            notify.write_json(self.config, value)
            with self.subTest(value=value), self.assertRaises(notify.NotifyError):
                notify.load_config(self.config)

    def test_allowed_urls_and_lark(self):
        for provider, url in URLS.items():
            notify.validate_url(provider, url)
        notify.validate_url("feishu", URLS["feishu"].replace("open.feishu.cn", "open.larksuite.com"))

    def test_reject_insecure_or_wrong_endpoints(self):
        cases = [
            URLS["wecom"].replace("https:", "http:"),
            URLS["wecom"].replace("qyapi.weixin.qq.com", "example.com"),
            URLS["wecom"].replace("qyapi.weixin.qq.com", "qyapi.weixin.qq.com.example.com"),
            URLS["wecom"].replace("https://", "https://user@"),
            URLS["wecom"].replace(".com/", ".com:8443/"),
            URLS["wecom"] + "#fragment",
            URLS["wecom"] + "&key=duplicate",
            URLS["wecom"] + "&other=value",
            URLS["wecom"].replace("/send?", "/upload_media?"),
            URLS["wecom"].replace("unit-test-only", ""),
            URLS["wecom"] + "\n",
            "https://[invalid",
        ]
        for url in cases:
            with self.subTest(url=url), self.assertRaisesRegex(notify.NotifyError, "invalid_webhook"):
                notify.validate_url("wecom", url)

    def test_wecom_payload_is_exact_plain_text(self):
        self.configure()
        channel = notify.load_config(self.config)["channels"]["work"]
        provider, url, payload, _ = notify.build_request(channel, "这里是通知")
        self.assertEqual(provider, "wecom")
        self.assertEqual(url, URLS["wecom"])
        self.assertEqual(payload, {"msgtype": "text", "text": {"content": "这里是通知"}})

    def test_feishu_signing_uses_empty_message(self):
        self.configure(provider="feishu", signing_secret_env="TEST_SIGN")
        channel = notify.load_config(self.config)["channels"]["work"]
        _, _, payload, _ = notify.build_request(channel, "hello", now=1234.5)
        expected = base64.b64encode(hmac.new(
            b"1234\nunit-test-signing-value", b"", hashlib.sha256
        ).digest()).decode()
        self.assertEqual(payload, {"msg_type": "text", "content": {"text": "hello"},
                                   "timestamp": "1234", "sign": expected})

    def test_dingtalk_signing_and_endpoint_identity(self):
        self.configure(provider="dingtalk", signing_secret_env="TEST_SIGN")
        channel = notify.load_config(self.config)["channels"]["work"]
        _, url, payload, identity = notify.build_request(channel, "hello", now=1234.5)
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
        expected = base64.b64encode(hmac.new(
            b"unit-test-signing-value", b"1234500\nunit-test-signing-value", hashlib.sha256
        ).digest()).decode()
        self.assertEqual(query["timestamp"], ["1234500"])
        self.assertEqual(query["sign"], [expected])
        self.assertEqual(payload, {"msgtype": "text", "text": {"content": "hello"}})
        self.assertEqual(identity, notify.build_request(channel, "hello", now=2345.6)[3])

    def test_endpoint_identity_normalizes_equivalent_urls(self):
        self.configure()
        channel = notify.load_config(self.config)["channels"]["work"]
        identity = notify.build_request(channel, "hello")[3]
        with patch.dict(os.environ, {"TEST_WECOM": URLS["wecom"].replace(
                "qyapi.weixin.qq.com", "QYAPI.WEIXIN.QQ.COM:443").replace("unit", "%75nit")}):
            self.assertEqual(identity, notify.build_request(channel, "hello")[3])

    def test_dry_run_never_sends_or_writes_state(self):
        self.configure()
        with patch.object(notify, "post") as post:
            result = self.send(dry_run=True)
        post.assert_not_called()
        self.assertEqual(result[0]["status"], "dry_run")
        self.assertFalse(self.state.exists())

    def test_all_destinations_preflight_before_send(self):
        self.configure()
        self.configure("alerts", "feishu")
        with patch.dict(os.environ, {"TEST_FEISHU": ""}), patch.object(notify, "post") as post:
            with self.assertRaisesRegex(notify.NotifyError, "credential_missing"):
                self.send(channels=["work", "alerts"])
        post.assert_not_called()
        self.assertFalse(self.state.exists())

    def test_unknown_channel_does_not_fallback(self):
        self.configure()
        with self.assertRaisesRegex(notify.NotifyError, "channel_not_found"):
            self.send(channels=["unknown"])
        self.assertFalse(self.state.exists())

    def test_nonempty_and_utf8_byte_limit(self):
        self.configure()
        for text in ("", " \n", "中" * 683, "x" * 2049):
            with self.subTest(length=len(text)), self.assertRaisesRegex(
                    notify.NotifyError, "text_required"):
                self.send(text=text, dry_run=True)
        self.assertEqual(self.send(text="中" * 682, dry_run=True)[0]["status"], "dry_run")
        self.assertEqual(self.send(text="x" * 2048, dry_run=True)[0]["status"], "dry_run")

    def test_channel_failure_isolated_and_output_sanitized(self):
        self.configure()
        self.configure("alerts", "feishu")
        with patch.object(notify, "post", side_effect=[notify.NotifyError("provider_rejected"), None]):
            results = self.send(channels=["work", "alerts"], event="completed", task_id="example")
        self.assertEqual([r["status"] for r in results], ["failed", "accepted"])
        self.assertNotIn("unit-test-only", json.dumps(results))

    def test_unexpected_transport_exception_isolated_and_redacted(self):
        self.configure()
        self.configure("alerts", "feishu")
        with patch.object(notify, "post", side_effect=[RuntimeError(URLS["wecom"]), None]):
            results = self.send(channels=["work", "alerts"])
        self.assertEqual([r["status"] for r in results], ["unconfirmed", "accepted"])
        self.assertNotIn(URLS["wecom"], json.dumps(results))

    def test_events_require_task_id_and_are_independently_deduplicated(self):
        self.configure()
        with self.assertRaisesRegex(notify.NotifyError, "event_requires_task_id"):
            self.send(event="completed")
        with patch.object(notify, "post") as post:
            for event in ("completed", "failed", "needs-input"):
                self.assertEqual(self.send(event=event, task_id="example")[0]["status"], "accepted")
                duplicate = self.send(text="changed wording", event=event, task_id="example")[0]
                self.assertEqual(duplicate["status"], "duplicate")
                self.assertEqual(duplicate["previous_status"], "accepted")
        self.assertEqual(post.call_count, 3)

    def test_unknown_delivery_is_not_retried(self):
        self.configure()
        with patch.object(notify, "post", side_effect=notify.NotifyError("delivery_unconfirmed")) as post:
            first = self.send(event="completed", task_id="example")
            second = self.send(event="completed", task_id="example")
        self.assertEqual(first[0]["status"], "unconfirmed")
        self.assertEqual(second[0]["previous_status"], "unconfirmed")
        post.assert_called_once()

    def test_rate_limit_20_per_rolling_minute_including_failures(self):
        self.configure()
        with patch.object(notify.time, "time", return_value=1000), patch.object(
                notify, "post", side_effect=notify.NotifyError("provider_rejected")) as post:
            for _ in range(20):
                self.assertEqual(self.send()[0]["status"], "failed")
            self.assertEqual(self.send()[0]["status"], "rate_limited")
        self.assertEqual(post.call_count, 20)
        with patch.object(notify.time, "time", return_value=1060), patch.object(notify, "post"):
            self.assertEqual(self.send()[0]["status"], "accepted")

    def test_rate_and_dedup_shared_by_aliases(self):
        self.configure()
        self.configure("same-bot")
        with patch.object(notify, "post") as post:
            results = self.send(channels=["work", "same-bot"], event="completed", task_id="example")
            self.assertEqual([r["status"] for r in results], ["accepted", "duplicate"])
            for _ in range(19):
                self.send(channels=["same-bot"])
            self.assertEqual(self.send()[0]["status"], "rate_limited")
        self.assertEqual(post.call_count, 20)

    def test_duplicate_channel_argument_sent_once(self):
        self.configure()
        with patch.object(notify, "post") as post:
            self.send(channels=["work", "work"])
        post.assert_called_once()

    def test_concurrent_reservations_cannot_exceed_rate_limit(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(
                lambda _: notify.reserve(self.state, "endpoint", None, 1000), range(25)
            ))
        self.assertEqual(results.count(None), 20)
        self.assertEqual(sum(r is not None and r["status"] == "rate_limited" for r in results), 5)

    def test_concurrent_events_are_reserved_once(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(
                lambda _: notify.reserve(self.state, "endpoint", "event", 1000), range(10)
            ))
        self.assertEqual(results.count(None), 1)
        self.assertEqual(sum(r is not None and r["status"] == "duplicate" for r in results), 9)

    def test_dedup_expires_after_24_hours(self):
        self.assertIsNone(notify.reserve(self.state, "endpoint", "event", 1000))
        self.assertEqual(notify.reserve(self.state, "endpoint", "event", 1001)["status"], "duplicate")
        self.assertIsNone(notify.reserve(self.state, "endpoint", "event", 87400))

    def test_state_contains_neither_body_nor_destination_nor_task_id(self):
        self.configure()
        with patch.object(notify, "post"):
            self.send(text="PRIVATE BODY EXAMPLE", event="completed", task_id="example-task")
        data = self.state.read_text(encoding="utf-8")
        for value in ("PRIVATE BODY EXAMPLE", URLS["wecom"], "example-task"):
            self.assertNotIn(value, data)

    def test_corrupt_state_fails_closed(self):
        self.configure()
        for state in ([], {"attempts": [], "events": {}},
                      {"attempts": {"example": [float("nan")]}, "events": {}}):
            notify.write_json(self.state, state)
            with patch.object(notify, "post") as post:
                result = self.send()
            self.assertEqual(result[0]["status"], "failed")
            post.assert_not_called()

    def test_finish_failure_preserves_success_and_does_not_retry(self):
        self.configure()
        with patch.object(notify, "post") as post, patch.object(
                notify, "finish", side_effect=OSError("synthetic")):
            first = self.send(event="completed", task_id="example")[0]
            second = self.send(event="completed", task_id="example")[0]
        self.assertEqual(first["status"], "accepted")
        self.assertEqual(first["state_warning"], "state_update_failed")
        self.assertEqual(second["previous_status"], "reserved")
        post.assert_called_once()

    def test_lock_does_not_get_removed_when_owned_elsewhere(self):
        self.state.with_name("state.json.lock").touch()
        with patch.object(notify.time, "monotonic", side_effect=[0, 4]):
            with self.assertRaisesRegex(notify.NotifyError, "state_locked"):
                with notify.locked(self.state):
                    self.fail("lock unexpectedly acquired")
        self.assertTrue(self.state.with_name("state.json.lock").exists())

    def test_post_requires_business_success_not_only_http_200(self):
        cases = [
            ("wecom", b'{"errcode":0,"errmsg":"ok"}', True),
            ("dingtalk", b'{"errcode":0}', True),
            ("feishu", b'{"code":0}', True),
            ("feishu", b'{"StatusCode":0}', True),
            ("feishu", b'{"code":1,"StatusCode":0}', False),
            ("wecom", b'{"errcode":123,"errmsg":"sensitive remote body"}', False),
            ("wecom", b'{"errcode":false}', False),
            ("wecom", b'{"errcode":"0"}', False),
            ("wecom", b'{}', False),
            ("wecom", b'[]', False),
            ("wecom", b'not-json', False),
            ("wecom", b'x' * 65537, False),
        ]
        for provider, body, success in cases:
            opener = self.response(body)
            with self.subTest(provider=provider, body=body[:100]), patch.object(
                    notify.urllib.request, "build_opener", return_value=opener):
                if success:
                    notify.post(provider, URLS[provider], {"text": "hello"})
                else:
                    with self.assertRaises(notify.NotifyError) as caught:
                        notify.post(provider, URLS[provider], {"text": "hello"})
                    self.assertNotIn("sensitive", str(caught.exception))

    def test_post_uses_json_utf8_timeout_and_no_redirect(self):
        opener = self.response(b'{"errcode":0}')
        with patch.object(notify.urllib.request, "build_opener", return_value=opener) as build:
            notify.post("wecom", URLS["wecom"], {"text": "通知"})
        request = opener.open.call_args.args[0]
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.get_header("Content-type"), "application/json")
        self.assertEqual(json.loads(request.data), {"text": "通知"})
        self.assertEqual(opener.open.call_args.kwargs["timeout"], 10)
        self.assertIsInstance(build.call_args.args[0], notify.NoRedirect)
        self.assertIsNone(notify.NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.com"))

    def test_http_errors_and_timeout_are_sanitized_without_retry(self):
        errors = [
            (urllib.error.HTTPError(URLS["wecom"], 429, URLS["wecom"], {}, None), "http_rate_limited"),
            (urllib.error.HTTPError(URLS["wecom"], 302, URLS["wecom"], {}, None), "http_rejected"),
            (urllib.error.URLError(URLS["wecom"]), "delivery_unconfirmed"),
            (TimeoutError(URLS["wecom"]), "delivery_unconfirmed"),
        ]
        for error, expected in errors:
            opener = Mock()
            opener.open.side_effect = error
            with self.subTest(expected=expected), patch.object(
                    notify.urllib.request, "build_opener", return_value=opener):
                with self.assertRaisesRegex(notify.NotifyError, expected):
                    notify.post("wecom", URLS["wecom"], {})
            opener.open.assert_called_once()

    def test_cli_list_and_dry_run_do_not_expose_values(self):
        self.configure()
        code, result = self.cli("list")
        self.assertEqual(code, 0)
        self.assertEqual(result, [{"channel": "work", "provider": "wecom"}])
        code, result = self.cli("send", "--channel", "work", "--message-stdin", "--dry-run")
        self.assertEqual(code, 0)
        self.assertEqual(result[0]["status"], "dry_run")

    def test_cli_failed_duplicate_exits_nonzero(self):
        self.configure()
        args = ("send", "--channel", "work", "--message-stdin",
                "--event", "failed", "--task-id", "example")
        with patch.object(notify, "post", side_effect=notify.NotifyError("delivery_unconfirmed")):
            self.assertEqual(self.cli(*args)[0], 1)
            code, result = self.cli(*args)
        self.assertEqual(code, 1)
        self.assertEqual(result[0]["status"], "duplicate")

    def test_cli_successful_duplicate_exits_zero(self):
        self.configure()
        args = ("send", "--channel", "work", "--message-stdin",
                "--event", "completed", "--task-id", "example")
        with patch.object(notify, "post"):
            self.assertEqual(self.cli(*args)[0], 0)
            self.assertEqual(self.cli(*args)[0], 0)

    def test_cli_top_level_exception_does_not_leak(self):
        with patch.object(notify, "load_config", side_effect=RuntimeError(URLS["wecom"])):
            code, result = self.cli("list")
        self.assertEqual(code, 1)
        self.assertEqual(result["error"], "operation_failed")

    def test_cli_invalid_arguments_do_not_echo_sensitive_values(self):
        output = io.StringIO()
        with redirect_stderr(output), self.assertRaises(SystemExit) as caught:
            notify.main(["configure", "--name", "work", "--provider", URLS["wecom"]])
        self.assertEqual(caught.exception.code, 2)
        self.assertNotIn(URLS["wecom"], output.getvalue())
        self.assertEqual(json.loads(output.getvalue())["error"], "invalid_arguments")

    def test_actual_cli_file_and_stdin_from_unrelated_directory(self):
        self.configure()
        message = self.home / "message.txt"
        message.write_text("这是通知", encoding="utf-8-sig")
        for source in (["--message-file", str(message)], ["--message-stdin"]):
            result = subprocess.run(
                [sys.executable, "-B", "-X", "utf8", str(SCRIPT), "--config", str(self.config),
                 "send", "--channel", "work", "--dry-run", *source],
                input="这是通知", text=True, encoding="utf-8", capture_output=True,
                cwd=self.home, timeout=10,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)[0]["status"], "dry_run")
        self.assertFalse(self.state.exists())

    @unittest.skipIf(os.name == "nt", "POSIX permissions, Windows uses inherited ACLs")
    def test_posix_state_and_config_permissions(self):
        self.configure()
        with patch.object(notify, "post"):
            self.send()
        self.assertEqual(self.config.stat().st_mode & 0o777, 0o600)
        self.assertEqual(self.state.stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()

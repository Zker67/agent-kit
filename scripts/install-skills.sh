#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
用法: install-skills.sh [选项] [目标目录]

选项:
  --dry-run   只打印将要执行的复制与删除，不写盘。
  --clean     复制前删除目标目录中名称以 pro- 开头、且不在本仓库 skills/ 内的子目录。
              只处理 pro- 前缀，不影响用户放在同一目录的其他 skill。
  -h, --help  显示本帮助。

目标目录省略时依次回落到 $CODEX_HOME/skills、$HOME/.codex/skills。
USAGE
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
source_dir="$repo_root/skills"

dry_run=0
clean=0
target_dir=""

# 参数顺序无关：选项与位置参数可任意穿插。
while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run) dry_run=1 ;;
    --clean)   clean=1 ;;
    -h|--help) usage; exit 0 ;;
    --) shift; [ "$#" -gt 0 ] && target_dir="$1" ;;
    -*) printf '未知选项: %s\n\n' "$1" >&2; usage >&2; exit 2 ;;
    *)
      if [ -n "$target_dir" ]; then
        printf '只接受一个目标目录，已收到第二个: %s\n' "$1" >&2
        exit 2
      fi
      target_dir="$1"
      ;;
  esac
  shift
done

if [ -z "$target_dir" ]; then
  if [ -n "${CODEX_HOME:-}" ]; then
    target_dir="$CODEX_HOME/skills"
  else
    target_dir="$HOME/.codex/skills"
  fi
fi

prefix=""
[ "$dry_run" -eq 1 ] && prefix="[dry-run] "

if [ "$dry_run" -eq 0 ]; then
  mkdir -p "$target_dir"
fi

# --clean：删除目标目录里已从仓库移除的 pro- 前缀 skill。
if [ "$clean" -eq 1 ]; then
  # 删除动作前校验目标路径非空且已存在，防止路径解析为空导致误删。
  if [ -z "$target_dir" ]; then
    printf '目标目录为空，拒绝执行清理。\n' >&2
    exit 1
  fi
  if [ -d "$target_dir" ]; then
    for existing in "$target_dir"/pro-*; do
      [ -d "$existing" ] || continue
      name="$(basename "$existing")"
      if [ ! -d "$source_dir/$name" ]; then
        printf '%sremove %s <- %s\n' "$prefix" "$name" "$existing"
        [ "$dry_run" -eq 0 ] && rm -rf "$existing"
      fi
    done
  fi
fi

for skill_dir in "$source_dir"/*; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  destination="$target_dir/$skill_name"

  # 先删除同名目录再复制，保证已从仓库删除的单个文件不残留。
  if [ "$dry_run" -eq 0 ]; then
    [ -n "$destination" ] && [ -d "$destination" ] && rm -rf "$destination"
    cp -R "$skill_dir" "$target_dir/"
  fi
  printf '%sinstall %s -> %s\n' "$prefix" "$skill_name" "$destination"
done

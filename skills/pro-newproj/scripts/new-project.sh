#!/usr/bin/env bash
# new-project.ps1 的 Bash 版，行为保持一致：默认拒绝非空目录；--merge 只补缺失文件，不覆盖已有内容。
set -euo pipefail

usage() {
  cat <<'USAGE'
用法: new-project.sh --name <project-name> [--target-root <parent-dir>] [--merge]

  --name         项目目录名，只允许字母、数字、点、下划线、连字符，且以字母或数字开头。
  --target-root  父目录，默认为当前目录。
  --merge        目标非空时只复制缺失的模板文件，并列出跳过的已有文件。
  -h, --help     显示本帮助。
USAGE
}

name=""
target_root="$PWD"
merge=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --name)
      [ "$#" -ge 2 ] || { printf -- '--name 需要参数\n' >&2; exit 2; }
      name="$2"; shift ;;
    --target-root)
      [ "$#" -ge 2 ] || { printf -- '--target-root 需要参数\n' >&2; exit 2; }
      target_root="$2"; shift ;;
    --merge) merge=1 ;;
    -h|--help) usage; exit 0 ;;
    *) printf '未知参数: %s\n\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

if ! printf '%s' "$name" | grep -Eq '^[A-Za-z0-9][A-Za-z0-9._-]*$'; then
  printf 'Invalid project name: %s\n' "$name" >&2
  exit 2
fi

skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
template_dir="$skill_dir/assets/base-project"

case "$target_root" in
  /*) ;;
  *) target_root="$PWD/$target_root" ;;
esac
project_dir="${target_root%/}/$name"

if [ ! -d "$template_dir" ]; then
  printf 'Bundled project template is missing: %s\n' "$template_dir" >&2
  exit 1
fi

if [ -f "$project_dir" ]; then
  printf 'Target is a file, not a directory: %s\n' "$project_dir" >&2
  exit 1
fi

if [ -d "$project_dir" ] && [ -n "$(ls -A "$project_dir")" ] && [ "$merge" -eq 0 ]; then
  printf 'Target is not empty: %s. Use --merge to add only missing template files.\n' "$project_dir" >&2
  exit 1
fi

template_files=()
while IFS= read -r -d '' file; do
  template_files+=("${file#"$template_dir"/}")
done < <(find "$template_dir" -type f -print0 | sort -z)

conflicts=()
for relative in "${template_files[@]}"; do
  if [ -e "$project_dir/$relative" ] || [ -L "$project_dir/$relative" ]; then
    conflicts+=("$relative")
  fi
done

if [ "${#conflicts[@]}" -gt 0 ] && [ "$merge" -eq 0 ]; then
  (IFS=','; printf 'Target contains template paths: %s\n' "${conflicts[*]}" >&2)
  exit 1
fi

mkdir -p "$project_dir"

copied=0
skipped=()
for relative in "${template_files[@]}"; do
  destination="$project_dir/$relative"
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    skipped+=("$relative")
    continue
  fi
  mkdir -p "$(dirname "$destination")"
  cp "$template_dir/$relative" "$destination"
  copied=$((copied + 1))
done

printf 'Project documentation scaffold: %s\n' "$project_dir"
printf 'Copied files: %s\n' "$copied"

if [ "${#skipped[@]}" -gt 0 ]; then
  printf 'Skipped existing files: %s\n' "${#skipped[@]}"
  printf '  %s\n' "${skipped[@]}"
fi

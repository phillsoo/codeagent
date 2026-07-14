#!/usr/bin/env python3
"""Export a reproducible, secret-free Hermes snapshot for version control."""
from __future__ import annotations

import json
import os
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HOME = Path(os.environ.get("HOME", "~")).expanduser()
HERMES_HOME = Path(os.environ.get("HERMES_HOME", HOME / ".hermes"))
REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "snapshot"

SECRET_KEY = re.compile(
    r"(^|_)(api_?key|token|secret|password|passwd|credential|private_?key|client_?secret|"
    r"bot_?token|app_?token|access_?token|refresh_?token|webhook_?url)($|_)", re.I
)
PRIVATE_ID_KEY = re.compile(r"^(chat_id|chat_name|thread_id|user_id|channel_id|team_id)$", re.I)
SECRET_VALUE = re.compile(
    r"(?:gh[opsu]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|"
    r"sk-[A-Za-z0-9_-]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|"
    r"\b[CUT][0-9][A-Z0-9]{8,}\b|\bocid1\.[A-Za-z0-9._-]+\b|\uc784\ud544\uc218)"
)
RUNTIME_KEYS = {
    "created_at", "updated_at", "next_run_at", "last_run_at", "last_status", "last_error",
    "last_delivery_error", "fire_claim", "completed", "paused_at", "paused_reason", "state",
}


def redact(value: Any, key: str = "") -> Any:
    if SECRET_KEY.search(key) or PRIVATE_ID_KEY.match(key):
        return "${REDACTED}"
    if isinstance(value, dict):
        return {k: redact(v, str(k)) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v, key) for v in value]
    if isinstance(value, str):
        value = value.replace(str(HOME), "${HOME}")
        return SECRET_VALUE.sub("${REDACTED}", value)
    return value


def load_structured(path: Path) -> Any:
    if path.suffix == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise SystemExit("PyYAML is required; run this with the Hermes Python environment") from exc
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def dump_structured(value: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".json":
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    else:
        import yaml  # type: ignore
        path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False), encoding="utf-8")


def copy_redacted(src: Path, dst: Path) -> None:
    if src.exists():
        dump_structured(redact(load_structured(src)), dst)


def copy_agents() -> list[str]:
    profiles = ["default"]
    for profile_dir in sorted((HERMES_HOME / "profiles").glob("*")):
        if profile_dir.is_dir():
            profiles.append(profile_dir.name)
    for name in profiles:
        base = HERMES_HOME if name == "default" else HERMES_HOME / "profiles" / name
        target = OUT / "agents" / name
        for filename in ("SOUL.md", "profile.yaml"):
            src = base / filename
            if src.exists():
                target.mkdir(parents=True, exist_ok=True)
                if src.suffix == ".yaml":
                    copy_redacted(src, target / filename)
                else:
                    text = SECRET_VALUE.sub("${REDACTED}", src.read_text(encoding="utf-8"))
                    (target / filename).write_text(text.replace(str(HOME), "${HOME}"), encoding="utf-8")
        copy_redacted(base / "config.yaml", OUT / "config" / f"{name}.yaml")
    return profiles


def copy_skills() -> int:
    src = HERMES_HOME / "skills"
    dst = OUT / "skills"
    if not src.exists():
        return 0

    bundled_manifest = src / ".bundled_manifest"
    bundled: dict[str, str] = {}
    if bundled_manifest.exists():
        for line in bundled_manifest.read_text(encoding="utf-8").splitlines():
            if ":" in line:
                name, digest = line.split(":", 1)
                bundled[name] = digest
    dump_structured(
        {"note": "Bundled skills are restored by Hermes; only names and source digests are versioned here.",
         "skills": bundled},
        dst / "BUNDLED_SKILLS.json",
    )

    custom_dirs: list[Path] = []
    for skill_md in sorted(src.rglob("SKILL.md")):
        if any(part.startswith(".") for part in skill_md.relative_to(src).parts):
            continue
        header = skill_md.read_text(encoding="utf-8", errors="ignore")[:2000]
        match = re.search(r"^name:\s*[\"']?([^\"'\n]+)", header, re.M)
        name = match.group(1).strip() if match else skill_md.parent.name
        if name not in bundled:
            custom_dirs.append(skill_md.parent)

    for skill_dir in custom_dirs:
        target = dst / skill_dir.relative_to(src)
        shutil.copytree(
            skill_dir,
            target,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns(
                "__pycache__", "*.pyc", ".usage.json", ".curator_backups", ".curator_state",
                ".hub", ".bundled_manifest", "*.lock", "validation-*.log"
            ),
        )

    count = 0
    for path in dst.rglob("*"):
        if path.is_file():
            count += 1
            if path.stat().st_size <= 5_000_000:
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                path.write_text(SECRET_VALUE.sub("${REDACTED}", text).replace(str(HOME), "${HOME}"), encoding="utf-8")
    return count


def copy_automation() -> int:
    src = HERMES_HOME / "cron" / "jobs.json"
    if not src.exists():
        return 0
    data = load_structured(src)
    jobs = []
    for raw in data.get("jobs", []):
        job = {k: v for k, v in raw.items() if k not in RUNTIME_KEYS and k != "origin"}
        repeat = job.get("repeat")
        if isinstance(repeat, dict):
            repeat.pop("completed", None)
        jobs.append(redact(job))
    dump_structured({"jobs": jobs}, OUT / "automation" / "cron.jobs.sanitized.json")
    return len(jobs)


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    profiles = copy_agents()
    skill_files = copy_skills()
    jobs = copy_automation()
    copy_redacted(
        HERMES_HOME / "kanban" / "boards" / "astra-organization" / "board.json",
        OUT / "organization" / "board.json",
    )
    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "${HOME}/.hermes",
        "profiles": profiles,
        "skill_files": skill_files,
        "cron_jobs": jobs,
        "repository_policy": "secret-free reproducible configuration snapshot",
        "excluded": [
            "credentials and auth files", "environment secret files", "sessions and memories",
            "logs, caches, databases and process state", "astra-organization operational artifacts",
            "Hermes source checkout and virtual environment",
        ],
    }
    (REPO / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

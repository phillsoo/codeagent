#!/usr/bin/env python3
"""Validate the skill and OCI CLI command paths without making OCI API calls."""

import argparse
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess

try:
    import yaml
except ImportError:
    yaml = None

parser = argparse.ArgumentParser()
parser.add_argument(
    "--inject-oci-path",
    metavar="PATH",
    help="add one literal command path to the local --help smoke (negative-test aid)",
)
args = parser.parse_args()

root = Path(__file__).resolve().parents[1]
text = (root / "SKILL.md").read_text(encoding="utf-8")
assert text.startswith("---\n")
end = text.find("\n---\n", 4)
assert end > 4 and text[end + 5:].strip()
front = text[4:end]
if yaml:
    fm = yaml.safe_load(front)
    assert fm["name"] == "oci-cloud-architect-operations"
    assert 0 < len(fm["description"]) <= 1024
else:
    assert re.search(r"^name:\s*oci-cloud-architect-operations$", front, re.M)
    assert re.search(r"^description:\s*", front, re.M)
assert len(text) <= 100_000

refs = set(re.findall(r"`(references/[^`]+\.md)`", text))
missing = [path for path in sorted(refs) if not (root / path).is_file()]
assert not missing, f"missing linked references: {missing}"
all_refs = list((root / "references").glob("*.md"))
assert len(all_refs) >= 10
for token in ["BLOCKED", "least privilege", "rollback", "Budget", "read-only", "검수자"]:
    assert token.lower() in text.lower(), token

# Check all four scenarios independently. A visible Gate map prevents complete
# prose in one scenario from masking a missing operational stage in another.
scenario_text = (root / "references" / "scenarios.md").read_text(encoding="utf-8")
scenario_sections = re.findall(
    r"^## ([1-4])\.[^\n]*\n(.*?)(?=^## |\Z)", scenario_text, re.M | re.S
)
assert [number for number, _ in scenario_sections] == ["1", "2", "3", "4"], "expected scenarios 1-4"
scenario_gates = ("intake", "discovery", "approval", "implement", "verification", "rollback")
for number, body in scenario_sections:
    lowered = body.lower()
    assert "**gate map:**" in lowered, f"scenario {number} has no explicit Gate map"
    missing_gates = [gate for gate in scenario_gates if gate not in lowered]
    assert not missing_gates, f"scenario {number} missing gates: {missing_gates}"
assert "네 핵심 scenario" in scenario_text, "static criteria must describe all four scenarios"

# Extract only fenced shell examples. Each line is reduced to literal command
# path tokens before the first option, so placeholders and option values are
# never expanded or sent to OCI. The only execution is `oci <path> --help`.
fence_re = re.compile(r"```(?:bash|sh|shell)\s*\n(.*?)```", re.I | re.S)
safe_part_re = re.compile(r"^[a-z0-9][a-z0-9-]*$")
read_only_leaves = {"get", "list", "structured-search"}
command_paths = set()
markdown_files = [root / "SKILL.md", *sorted(all_refs), root / "README.md"]
oci_examples = 0
for document in markdown_files:
    for block in fence_re.findall(document.read_text(encoding="utf-8")):
        logical = ""
        for raw_line in block.splitlines():
            stripped = raw_line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            logical = f"{logical} {stripped}".strip()
            if logical.endswith("\\"):
                logical = logical[:-1].rstrip()
                continue
            argv = shlex.split(logical, posix=True)
            logical = ""
            if not argv or argv[0] != "oci":
                continue
            oci_examples += 1
            path = []
            for part in argv[1:]:
                if part.startswith("-"):
                    break
                assert safe_part_re.fullmatch(part), (
                    f"unsafe/dynamic OCI command path in {document}: {part!r}"
                )
                path.append(part)
            assert path, f"missing OCI command path in {document}"
            assert path[-1] in read_only_leaves, (
                f"non-read-only fenced OCI example in {document}: {' '.join(path)}"
            )
            command_paths.add(tuple(path))
        assert not logical, f"unterminated continuation in {document}"
assert oci_examples, "no fenced OCI examples found"

if args.inject_oci_path:
    injected = tuple(shlex.split(args.inject_oci_path, posix=True))
    assert injected and all(safe_part_re.fullmatch(part) for part in injected), (
        "injected path must contain literal OCI command tokens only"
    )
    command_paths.add(injected)

oci = shutil.which("oci")
assert oci, "oci executable not found"
help_env = os.environ.copy()
help_env.update({"PAGER": "cat", "LC_ALL": "C"})
help_failures = []
for path in sorted(command_paths):
    result = subprocess.run(
        [oci, *path, "--help"],
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
        timeout=20,
        env=help_env,
        check=False,
    )
    if result.returncode != 0:
        help_failures.append(
            f"oci {' '.join(path)} --help (exit {result.returncode}): {result.stderr.strip()}"
        )
assert not help_failures, "OCI command-path help failures:\n" + "\n".join(help_failures)

print(
    f"PASS skill={root/'SKILL.md'} chars={len(text)} linked_refs={len(refs)} "
    f"total_refs={len(all_refs)} yaml={bool(yaml)} scenarios={len(scenario_sections)} "
    f"oci_examples={oci_examples} oci_help_paths={len(command_paths)} api_calls=0"
)

#!/usr/bin/env python3
"""P05-CP-STUDENT-01 local capability discovery.

Standard-library only. Reports local tool availability/version metadata without
reading API credentials, tokens, user names, hostnames, home directories, or
cloud account data.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "config" / "capabilities.yaml"


def load_catalog(path: Path = CATALOG_PATH) -> dict[str, Any]:
    # JSON is a valid YAML 1.2 subset and keeps this checkpoint dependency-free.
    return json.loads(path.read_text(encoding="utf-8"))


def _first_line(value: str) -> str:
    line = value.strip().splitlines()[0] if value.strip() else ""
    return line[:200]


def _command_version(command: str, args: list[str]) -> tuple[bool, str | None]:
    if shutil.which(command) is None:
        return False, None
    try:
        completed = subprocess.run(
            [command, *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return True, None
    output = completed.stdout or completed.stderr
    return True, _first_line(output) or None


def _detect_wsl() -> tuple[bool, str | None]:
    markers: list[str] = []
    if os.environ.get("WSL_INTEROP"):
        markers.append("WSL_INTEROP")
    if os.environ.get("WSL_DISTRO_NAME"):
        markers.append("WSL_DISTRO_NAME")

    try:
        proc_version = Path("/proc/version").read_text(encoding="utf-8").lower()
    except (OSError, UnicodeDecodeError):
        proc_version = ""

    if "microsoft" in proc_version or "wsl" in proc_version:
        markers.append("/proc/version")

    if not markers:
        return False, None
    return True, "detected via " + ", ".join(sorted(set(markers)))


def probe_capability(capability: dict[str, Any]) -> dict[str, Any]:
    probe = capability["probe"]
    available: bool | None
    version: str | None = None

    if probe == "platform":
        available = True
        version = f"{platform.system()} {platform.release()}".strip()
        status = "PASS"
    elif probe == "python_runtime":
        available = True
        version = platform.python_version()
        status = "PASS"
    elif probe == "wsl":
        available, version = _detect_wsl()
        status = "PASS" if available else "NOT_AVAILABLE"
    elif probe == "command":
        available, version = _command_version(
            capability["command"],
            list(capability.get("version_args", [])),
        )
        status = "PASS" if available else "NOT_AVAILABLE"
    elif probe == "external_not_probed":
        available = None
        status = "UNKNOWN_EXTERNAL"
    else:
        raise ValueError(f"Unsupported probe: {probe}")

    return {
        "id": capability["id"],
        "label": capability["label"],
        "class": capability["class"],
        "scope": capability["scope"],
        "status": status,
        "available": available,
        "version": version,
        "required_for_local_ready": bool(
            capability.get("required_for_local_ready", False)
        ),
        "persistent_dependency_allowed": bool(
            capability.get("persistent_dependency_allowed", False)
        ),
    }


def build_baseline(catalog: dict[str, Any]) -> dict[str, Any]:
    capabilities = [probe_capability(item) for item in catalog["capabilities"]]
    required_local = [
        item
        for item in capabilities
        if item["scope"] == "local" and item["required_for_local_ready"]
    ]
    ready = all(item["status"] == "PASS" for item in required_local)

    return {
        "checkpoint": catalog["checkpoint"],
        "name": catalog["name"],
        "direct_spend_usd": catalog["policy"]["direct_spend_usd"],
        "paid_services_auto_enabled": catalog["policy"]["auto_enable_paid_services"],
        "secrets_exposed": 0,
        "local_foundation_ready": ready,
        "verdict": "LOCAL_FOUNDATION_READY" if ready else "LOCAL_FOUNDATION_PARTIAL",
        "capabilities": capabilities,
    }


def render_human(baseline: dict[str, Any]) -> str:
    rows = ["KIANGANA 2.0 — STUDENT TECHNOLOGY BASELINE", ""]
    for item in baseline["capabilities"]:
        if item["scope"] != "local":
            continue
        suffix = f" | {item['version']}" if item["version"] else ""
        rows.append(f"{item['label']:<28} {item['status']}{suffix}")

    rows.extend(
        [
            "",
            f"DIRECT COST USD             {baseline['direct_spend_usd']}",
            f"SECRETS EXPOSED             {baseline['secrets_exposed']}",
            "",
            "VERDICT",
            baseline["verdict"],
        ]
    )
    return "\n".join(rows)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Discover the local #0$ KIANGANA 2.0 technology baseline."
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of the human report.",
    )
    args = parser.parse_args(argv)

    baseline = build_baseline(load_catalog())
    if args.json:
        print(json.dumps(baseline, indent=2, sort_keys=True))
    else:
        print(render_human(baseline))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

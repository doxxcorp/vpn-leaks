"""Per-run manifest (run.json)."""

from __future__ import annotations

import platform
import subprocess
import sys
from typing import Any

from pydantic import BaseModel, Field

from vpn_leaks.models import RunnerEnv, utc_now_iso


class RunManifest(BaseModel):
    run_id: str
    created_utc: str = Field(default_factory=utc_now_iso)
    git_sha: str | None = None
    vpn_provider: str
    tool_versions: dict[str, str] = Field(default_factory=dict)
    runner_env: RunnerEnv = Field(default_factory=RunnerEnv)


def _git_sha() -> str | None:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if out.returncode == 0:
            return out.stdout.strip()
    except OSError:
        pass
    return None


def build_manifest(*, run_id: str, vpn_provider: str) -> RunManifest:
    return RunManifest(
        run_id=run_id,
        git_sha=_git_sha(),
        vpn_provider=vpn_provider,
        tool_versions={
            "python": sys.version.split()[0],
        },
        runner_env=RunnerEnv(
            os=platform.system() + " " + platform.release(),
            kernel=platform.release(),
            python=sys.version,
        ),
    )


def manifest_to_json(m: RunManifest) -> dict[str, Any]:
    return m.model_dump(mode="json")

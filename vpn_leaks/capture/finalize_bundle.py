"""Attach final PCAP + pcap_summary into each fresh normalized.json for this run."""

from __future__ import annotations

import json
import shutil
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from vpn_leaks.capture.session import finalize_stop
from vpn_leaks.checks.pcap_summarize import summarize_pcap_file
from vpn_leaks.config_loader import repo_root
from vpn_leaks.models import CaptureSessionFinalize, NormalizedRun


def finalize_capture_and_merge(
    *,
    run_root: Path,
    fresh_norm_paths: list[Path],
    log: Callable[[str], None],
) -> dict[str, Any]:
    """Stop tcpdump, copy PCAP beside each processed location raw dir, summarize, patch JSON."""

    rr = repo_root()
    finalize_errors: list[str] = []

    desc, fin_stop_err = finalize_stop()
    if fin_stop_err:
        finalize_errors.append(fin_stop_err)

    outcome: dict[str, Any] = {
        "session": None,
        "errors": finalize_errors.copy(),
        "normalized_updated": [],
    }

    if desc is None:
        log("attach-capture: no tcpdump session was active to finalize.")
        outcome["errors"] = finalize_errors
        return outcome

    outcome["session"] = desc.to_json()
    src_pcap = Path(desc.pcap_path)
    if not src_pcap.is_file():
        msg = f"attach-capture: expected pcap missing at {src_pcap}"
        finalize_errors.append("pcap_missing_after_stop")
        log(msg)

    summary_full = summarize_pcap_file(src_pcap)

    targets = list(fresh_norm_paths)
    if not targets:
        log(
            "attach-capture: no new normalized outputs; "
            "PCAP saved under run-root raw/_capture_fallback/",
        )
        cap_dir = run_root / "raw" / "_capture_fallback"
        cap_dir.mkdir(parents=True, exist_ok=True)
        if src_pcap.is_file():
            dst = cap_dir / "session.pcap"
            shutil.copy2(src_pcap, dst)
            psum = cap_dir / "pcap_summary.json"
            psum.write_text(json.dumps(summary_full, indent=2), encoding="utf-8")
        try:
            src_pcap.unlink(missing_ok=True)
        except OSError:
            pass
        outcome["fallback_capture_dir"] = str(cap_dir.relative_to(rr))
        outcome["errors"] = finalize_errors
        return outcome

    for np in targets:
        loc_id = np.parent.name
        cap_dir = run_root / "raw" / loc_id / "capture"
        cap_dir.mkdir(parents=True, exist_ok=True)
        dst = cap_dir / "session.pcap"
        try:
            if src_pcap.is_file():
                shutil.copy2(src_pcap, dst)
        except OSError as e:
            finalize_errors.append(f"{loc_id}:copy:{e}")
            log(f"pcap copy failed: {e}")
        sj = cap_dir / "pcap_summary.json"
        sj.write_text(json.dumps(summary_full, indent=2), encoding="utf-8")

        rel_cap = str(cap_dir.relative_to(rr))
        nr = NormalizedRun.model_validate(json.loads(np.read_text(encoding="utf-8")))
        art = nr.artifacts.model_copy(update={"capture_dir": rel_cap})
        fin_patched = CaptureSessionFinalize(
            session_id=desc.session_id,
            finalized_at_utc=datetime.now(UTC).isoformat(),
            source_pcap_cache_path=str(desc.pcap_path),
            finalize_errors=list(finalize_errors),
        )
        nr = nr.model_copy(
            update={
                "artifacts": art,
                "pcap_derived": summary_full,
                "capture_finalize": fin_patched,
            }
        )
        np.write_text(nr.model_dump_json(indent=2), encoding="utf-8")
        outcome["normalized_updated"].append(str(np.relative_to(rr)))
        log(f"attach-capture: merged PCAP summary into {np}")

    try:
        if src_pcap.is_file():
            src_pcap.unlink(missing_ok=True)
    except OSError:
        pass

    outcome["errors"] = finalize_errors
    return outcome

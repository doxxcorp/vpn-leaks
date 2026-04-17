# Desk exposure transcript (template)

**Evidence tier:** **S** (systematic desk), not **O** (harness). Do not merge with `dnsleak/` or imply this answers **DNS-001** without labeling.

| Field | Value |
|-------|--------|
| UTC date | |
| Resolver used for `dig` (e.g. system / `@1.1.1.1`) | |
| Provider slug | |
| Apex domain(s) | |

## Phase 8 — raw transcript

Paste output from `scripts/desk_dns_audit.sh <apex> ...` or manual `dig` per [docs/website-exposure-methodology.md](../docs/website-exposure-methodology.md).

```text
(paste below)
```

## Phase 9 — third-party inventory (compiled)

| # | Company | How discovered | Role | What they can see |
|---|---------|------------------|------|-------------------|
| 1 | | NS / HAR / MX / SPF / … | | |
| 2 | | | | |

## Link to harness run (O)

- Run directory: `runs/<run_id>/`
- Relevant paths: `raw/<location_id>/competitor_probe/`, `surface_probe/` if used

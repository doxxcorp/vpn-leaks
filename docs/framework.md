# SPEC framework (question bank, coverage, findings)

Machine-readable config lives under [`configs/framework/`](../configs/framework/):

| File | Role |
|------|------|
| [`questions.yaml`](../configs/framework/questions.yaml) | Question IDs, category, text, testability class (SPEC §9) |
| [`test_matrix.yaml`](../configs/framework/test_matrix.yaml) | Sparse mapping of question IDs to test methods, tools, evidence expectations (SPEC §10) |
| [`classification_rules.yaml`](../configs/framework/classification_rules.yaml) | Domain suffix / override rules for endpoint labels (SPEC §12) |

## Synthesis

Each successful `vpn-leaks run` (unless `--no-framework`) embeds a `framework` object in `locations/<id>/normalized.json` with:

- **findings** — structured rows (severity, confidence, observed vs inferred)
- **question_coverage** — one record per question in `questions.yaml`
- **risk_scores** — rollup severities (SPEC §17)
- **observed_endpoints** — hosts from `services_contacted` and competitor web probes, classified via rules

Implementations: [`vpn_leaks/framework/`](../vpn_leaks/framework/).

## Provider YAML extensions

- **`surface_urls`** — list of `{ page_type, url }` entries; triggers Playwright HAR under `raw/<location_id>/surface_probe/` (SPEC §13.5). See [`configs/vpns/example.yaml`](../configs/vpns/example.yaml).

## CLI flags

| Flag | Behavior |
|------|----------|
| `--no-framework` | Skip synthesis (smaller JSON, no coverage rows) |
| `--capture-baseline` | Write `raw/baseline.json` at run start (disconnect VPN first for a true ISP baseline) |
| `--transition-tests` | Poll exit IP across disconnect/reconnect (`raw/<location_id>/transitions.json`); skipped for `manual_gui` |

## Reports

`vpn-leaks report --provider <slug>` includes an **Executive summary (SPEC framework)** section when any included `normalized.json` has a `framework` block.

### HTML dashboard

`VPNs/<SLUG>.html` is generated as a **visual-first** page: risk strip, per-location cards, leak summary chips, third-party / competitor signals when present, SPEC questions grouped by category (expandable), the coverage bar and **exposure graph** (same data as `vpn-leaks graph-export`), and the full markdown-derived narrative **collapsed** under **Full narrative export (markdown-derived)**. Styles and the doxx.net isotype are bundled from [`vpn_leaks/reporting/static/`](../vpn_leaks/reporting/static/) (design tokens aligned with the sibling [`style`](https://github.com/doxxcorp/style) repo; no Keystone fetch at report time).

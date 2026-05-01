# Competitive capture playbook

Two-command operator flow: **`capture start`** before signup/install, then **`vpn-leaks run --attach-capture`** on-VPN to run the full harness, stop capture, summarize PCAP, and merge into reports. **No Wireshark** (including `tshark`).

## Implemented in-tree (baseline)

Session-aware CLI: **`vpn-leaks capture start|status|abort`**, **`run --attach-capture`**, **`run --with-pcap`**, **`vpn-leaks pcap-summarize`**, PCAP under **`runs/<id>/raw/<location_id>/capture/`**, merge **`pcap_derived`** into **`normalized.json`**, report + **`graph-export`** integration ( **`graph_schema` 1.1** PCAP edges).

**Remaining / optional backlog:** JA3/JA4 pinning in **`[pcap]`** extra; advanced tcpdump rotation; reference provider YAML tweaks as vendors change URLs.

---

## Choosing a PCAP mode

| Approach | PCAP starts | Signup/install traffic in PCAP | Second command nuances |
|-----------|-------------|-----------------------------------|-------------------------|
| **`capture start` → `run --attach-capture`** | Before signup (you run **`capture start`** first) | Yes (full funnel) | Requires **active session** descriptor; **`--attach-capture`** stops tcpdump at end of **`run`** |
| **`run --with-pcap`** | When **`run`** begins (**harness-managed** tcpdump) | Only what happens during **CLI run** window | Cannot combine with **`--attach-capture`**; abort any stray **`capture start`** session first |

**Repair:** **`vpn-leaks pcap-summarize <path/to/file.pcap>`** emits **`pcap_summary.json`** without re-running benchmarks.

---

## Implementation backlog

- **utm-vm-per-provider:** UTM baseline image + clone workflow; host prep checklist (this document §Golden base VM).

---

## Repo strategy—capture lives in vpn-leaks

**This repo is the single canonical codebase** for competitive evaluation: `runs/`, `normalized.json`, HAR/`surface_probe`, `competitor_probe`, automated **website exposure methodology**, reports, **`graph-export`**, and **PCAP capture + summarization**.

**Authoritative companion docs:** [HANDOFF.md](../HANDOFF.md) (repo map, CLI, artifacts), [website-exposure-methodology.md](website-exposure-methodology.md) (website + DNS infrastructure desk methodology), [methodology.md](methodology.md), [data-dictionary.md](data-dictionary.md).

### What “capture as part of vpn-leaks” means (concrete integrations)

**Primary operator UX (two commands per campaign):**

1. **`vpn-leaks capture start`** — Spawns **`tcpdump`** on the chosen interface (**`-i` / `--interface`**, default from **`VPN_LEAKS_CAPTURE_INTERFACE`** or **`en0`**), writes a **session descriptor** (JSON under **`.vpn-leaks/capture/`**: `session_id`, `pid`, `pcap_path`, `interface`, `started_at_utc`, optional `bpf`). PCAP grows in cache until **`run`** finalizes (**`run_id`** did not exist at capture start).
2. **Human window** — browser signup, download/install vendor app, connect VPN (all traffic **including pre-VPN marketing + installer callbacks** lands in the same PCAP).
3. **`vpn-leaks run --provider <slug> --skip-vpn --attach-capture`** — **second command**: runs the **full existing harness** (leak tests, `competitor_probe`, `surface_urls`, policy, yourinfo, attribution, …) **while tunnel is up**. On **exit** (success or controlled failure): **stop tcpdump** from the active session descriptor, **rotate/close** the PCAP, **move or hardlink** it into `runs/<run_id>/raw/<location_id>/capture/*.pcap`, invoke **`pcap_summary`**, merge into **`normalized.json`**, then teardown session file. If **no** active capture, `run` behaves exactly as today.

**Helpers:** **`vpn-leaks capture status`** (active session + byte size), **`vpn-leaks capture abort`** (**`--keep-pcap`** optional). Interface default: env **`VPN_LEAKS_CAPTURE_INTERFACE`** or **`en0`**.

**Alternate path:** **`vpn-leaks run --with-pcap`** — harness starts **`tcpdump`** at run start (**no signup window** unless you overlap manually); merges the same **`pcap_derived`** block at finalize. Prefer **`attach-capture`** for full-funnel campaigns.

**PCAP summarization (shipping):** [`vpn_leaks/checks/pcap_summarize.py`](../vpn_leaks/checks/pcap_summarize.py) + CLI **`vpn-leaks pcap-summarize`** — **dpkt** only; **`pcap_summary.json`** includes flow samples, TLS SNI (ClientHello heuristic), UDP/53 DNS names, QUIC/opaque TLS hints and explicit **`limits`**. **`ja3_ja4`** array reserved until optional tooling lands in **`[pcap]`** extra.

**Report + graph fusion (shipping):** **`pcap_derived`** on **`normalized.json`**, Jinja rollup subsection in **`vpn-leaks report`**, and **`graph-export`** PCAP-related edges (**`graph_schema` 1.1**).

This playbook documents bpf defaults, “no Wireshark” policy, and interpretive limits (encrypted DNS, ESNI/ECH blindness). **Dependencies:** PCAP parsing uses **`dpkt`** (declared in **`pyproject.toml`**). **Never** Wireshark/mitmshark/tshark or **mitmproxy** on the standard operator path.

**Out of scope for bundling:** GUI TLS-intercept tools (e.g. Proxyman)—not part of `vpn-leaks` automation.

---

## What the output is (files and reports you keep)

You end up with **repeatable evidence bundles per provider** and **rollups**, not a single vague “analysis.”

**Delivered today by vpn-leaks** (per [HANDOFF.md](../HANDOFF.md)); capture features above **extend** this tree—in place—not a second product:

- **Per run folder** `runs/<run_id>/` with `normalized.json` (canonical machine-readable record), `summary.md`, and `raw/<location_id>/` artifacts: IP/DNS/WebRTC/IPv6 checks, attribution (RIPEstat / Team Cymru / PeeringDB), privacy policy fetch + hash, optional **yourinfo.ai** HAR/snapshot, **competitor_probe** (DNS of declared domains, portal HTTPS checks, transit probes, stray JSON), **surface_probe** HARs + `har_summary.json` when you list `surface_urls` in the provider YAML.
- **Rollup after one or more runs:** `vpn-leaks report --provider <slug>` → **`VPNs/<SLUG>.md`** and **`VPNs/<SLUG>.html`** (dashboard + Website/DNS surface section + embedded 3D graph when data exists).
- **Graph export:** `vpn-leaks graph-export --provider <slug> -o exposure-graph.json` → feed [viewer/](../viewer/).

**Desk methodology (DNS/email supply chain):** Automated projection in **`normalized.json`** → **`website_exposure_methodology`** during **`vpn-leaks run`**; authoritative definitions and manual deepening (transcripts **`S`**) in [website-exposure-methodology.md](website-exposure-methodology.md).

**Operational polish:** Prefer recording harness **git SHA** / hostname in **`run.json`** when available; note tester geography when CDN POP interpretation matters.

- **Raw PCAP** via **`tcpdump` only** (no Wireshark family); summarize with **`vpn-leaks`** (**`dpkt`**) — see **Choosing a PCAP mode** above.

---

## UTM VM discipline (locked in)

Use **one clean UTM macOS VM per competitor** (disk image never mixes Nord vs Mullvad) so PCAP/HAR stay attributable.

- **Several exits for the same competitor:** revert VM from a **golden template snapshot** between cities for strict isolation **or** accept cache from prior connects and document it.
- **macOS:** required for evaluating **vendor VPN apps** bundled for Mac; harness stack runs there too.

---

## Golden base VM — full setup (build once in UTM, then clone each run)

Bake **one** “golden” macOS VM in UTM, **power off**, **duplicate/clone** whenever you want a fresh research session. Below is everything to run **on that base image exactly once**—clones inherit it.

**Golden image assumptions:** macOS **guest** GUI install completed; primary local admin account (**no** iCloud / Apple Media / Analytics sign-in recommended so base stays quiet—optional). Use **aarch64 Apple Silicon guests** matching your silicon host when possible for speed.

### Base-image checklist (terminal commands in order)

**1 — Apple CLI tools**

```bash
xcode-select --install
```

Complete GUI installer reboot if required. Confirms **`git`**.

**Built-ins you rely on:** `dig`, `whois`, **`/usr/sbin/tcpdump`** (no extra install).

**2 — Install Homebrew** (unless already present)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Run the snippet Homebrew prints (eval `brew shellenv` …) so `brew` is on **`PATH`** in new Terminal tabs—add those lines to `~/.zprofile` **on the golden image** when Brew tells you to.

**3 — Packages via Brew**

```bash
brew install python@3.12 git jq
```

**Forbidden on base image:** anything **Wireshark** (`brew install --cask wireshark`), **`tshark`**, **`wireshark-cli`**. PCAP review is fully in **vpn-leaks** code paths.

**4 — vpn-leaks harness + Python venv**

Substitute `<REPO_URL>` (`git@github.com:doxxcorp/vpn-leaks.git`, etc.)—ensure SSH keys or HTTPS PAT work **before** cloning on the golden VM.

```bash
mkdir -p ~/src && cd ~/src
git clone <REPO_URL> vpn-leaks
cd vpn-leaks

python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"

playwright install chromium
```

Matches [HANDOFF.md](../HANDOFF.md) baseline.

**5 — Smoke tests**

```bash
source ~/src/vpn-leaks/.venv/bin/activate
vpn-leaks --help
which tcpdump python3.12
/usr/sbin/tcpdump -h | head -n 1
```

**6 — Optional shell convenience (golden image)**

Append to `~/.zshrc` (or `~/.zprofile` if you prefer login shells only):

```bash
# vpn-leaks venv
[[ -f "$HOME/src/vpn-leaks/.venv/bin/activate" ]] && source "$HOME/src/vpn-leaks/.venv/bin/activate"
```

**7 — tcpdump privileges**

`tcpdump` typically needs **root** on macOS. Pick one org policy:

- Interactively enter **sudo** when the harness invokes capture, **or**
- Allow **passwordless sudo** for **only** `/usr/sbin/tcpdump` (narrow `sudoers` fragment)—only if your security policy permits.

Do **not** store sudo passwords in scripts.

**8 — SSH for `git pull` on clones**

For private `vpn-leaks`, run `ssh -T git@github.com` once on the **golden** image and accept host key so clones work.

**9 — Freeze the golden template**

- Run **Software Update** until you are happy, then **avoid ad-hoc `brew upgrade`** on golden so clones stay reproducible; document **macOS build + brew lock** in your lab notes.
- **Shut down** the guest cleanly.
- In **UTM:** **Duplicate** this VM (or snapshot + clone per UTM feature you use). Name the original something like **`macos-vpn-research-GOLDEN-DO-NOT-DEPLOY`**.

### On every **cloned** VM (before a benchmark)

1. **Boot the clone**; optionally rename host in **System Settings → General → Sharing** so `run.json` hostname reflects the campaign.
2. **`cd ~/src/vpn-leaks && git fetch && git checkout <tag-or-branch> && git pull`** then **`source .venv/bin/activate`**, **`pip install -e ".[dev]"`** if `pyproject.toml` changed, **`playwright install chromium`** if Playwright bumped.
3. **Command A — start PCAP before any provider interaction:** `vpn-leaks capture start [--interface en0]`.
4. In browser: **sign up / checkout** as needed; **download and install** the vendor app; **connect** to your chosen exit.
5. **Command B — full benchmark on-VPN:** `vpn-leaks run --provider <slug> --skip-vpn --attach-capture [--force …]` (stops capture, summarizes, writes `runs/<run_id>/`).

**Never** `brew upgrade` on a clone mid-campaign if you need apples-to-apples comparisons—only update when intentionally rebasing methodology.

### JA3/JA4 / PCAP analytics on the base image

**`dpkt`** is installed with **`pip install -e ".[dev]"`** via `pyproject.toml`. Still **no Wireshark** / **tshark** / **mitmproxy** on the golden path.

---

## What you do vs automation

**Operator loop:** **Command 1** starts capture → **you** signup / install / connect → **Command 2** runs every harness check **on-VPN**, then **stops capture + summarizes + lands artifacts** in `runs/`.

### Checklist — human steps (today)

1. **Duplicate** your **golden UTM VM** (fresh clone per campaign); **do not** reuse one clone across competitors if you need clean attribution.
2. **First-login hygiene** was done on golden; on clone: stay **signed out** of personal Apple ID unless a test requires it.
3. **Toolchain inherited from golden;** on clone only **`git pull` + `pip install -e ".[dev]"` + `playwright install chromium`** when the repo changes.
4. **Edit/add** `configs/vpns/<slug>.yaml` for new competitors (**domains**, `surface_urls`, `policy_urls`, `competitor_probe`).
5. **Command 1 — start capture** (before touching the provider):

```bash
vpn-leaks capture start [--interface en0]
```

6. **Browser + app (human):** account creation, payment if required, **download + install** official app, **choose exit + Connect** (CAPTCHA/OTP/billing stay **you**).
7. **Command 2 — full automated benchmark + PCAP finalize** (VPN must still be connected):

```bash
vpn-leaks run --provider <slug> --skip-vpn --attach-capture [--force ...]
```

Harness runs **all** automated phases; on completion it **stops tcpdump**, runs **`pcap_summary`**, merges into **`normalized.json`**. (Exact flag names ship with implementation; **`--with-pcap`** remains the short-window alternative.)

8. **More cities:** **Command 1** again (or new clone) → reconnect elsewhere → **Command 2** again.
9. **Publishing:** `git` add/commit `runs/`, lift artifacts off the VM as needed.
10. **Executive wording** (“who can see what”)—human reviewer; may draft from normalized outputs.

### Automated by vpn-leaks + capture extensions

Including: **session-scoped PCAP** spanning signup through benchmark; competitor DNS probing; **`surface_urls` Playwright** + **HAR summaries**; leak URLs; **yourinfo.ai** if enabled; **policy** fetch; RIPEstat / Cymru / PeeringDB attribution; automated **website-exposure methodology** (Phases 1–9 desk bundle in `normalized.json`); **`pcap_summary` + report fusion**; **`vpn-leaks report`** + **`graph-export`**; optional **JA** fingerprints from **`pcap_summary`** when enabled.

**Rare escape hatch:** one **manual Safari** capture if Cloudflare defeats Playwright—drop HAR under `runs/.../manual/` and annotate.

---

## Implementer mapping (phases aligned with codebase)

Treat each competitor as multiple **`runs/`** (`location_id`/exit-dependent). Rough mapping:

- **Phase 0:** UTM template + toolchain bootstrap (checklist steps 1–3 above).
- **Phase A:** `capture start` — long-lived PCAP (minus sudo password).
- **Phase B:** Human signup/install/connect — **PCAP includes marketing + installers + tunnel bring-up**.
- **Phase C:** `run --attach-capture` — harness phases + **`capture finalize`** inside same process.

---

## tcpdump + Python summarization (standard path)

- **tcpdump:** captures **all** IP packets visible to the NIC—ports, flows, timing.
- **Interpretation:** **`vpn-leaks pcap-summarize`** / in-run merge uses **dpkt** (SNI/DNS aggregates, optional JA math later)—**never** Wireshark/`tshark`.
- **Limits:** no decrypted HTTP bodies from this path; ECH/DoH blind spots must be labeled in `pcap_summary.json`.
- **Operational default:** session **tcpdump** from **`capture start`** through **`run --attach-capture`**; optional BPF on `capture start` if you need to trim volume.

---

## Post-run PCAP → report pipeline (implementation contract)

Triggered **automatically when `vpn-leaks run --attach-capture` finalizes** the active capture session **or** at end of **`run --with-pcap`** (**short-window mode**). Standalone repair: **`vpn-leaks pcap-summarize <path>`**.

1. **Inputs:** `.pcap` path(s), run + `location_id` metadata, optional interface name BPF echo in summary for audit.
2. **Processing:** deterministic Python parser emitting **`pcap_summary.json`** (+ optional compact `.csv` for diffing)—schema version field mandatory.
3. **Merge:** hydrate **`normalized.json`** `artifacts`/`extra`/`pcap_derived` (exact keying decided in `vpn_leaks/models.py`).
4. **Reports:** **`vpn-leaks report`** pulls merged data into **Markdown + HTML** (“PCAP-derived third parties”, “TLS SNI inventory”, “JA fingerprints observed”, “gaps: opaque flows”).
5. **Quality bar:** If parser fails, run **fails soft** with warning + empty section—never silent drop of PCAP file path.

---

## Automation boundary

Inside a **fresh clone**, you run **two CLI entrypoints**: **capture start**, then **`run … --attach-capture`** after manual install. Remaining friction: sudo for tcpdump, CAPTCHA/account flows, vendor UI for connect, reviewer narrative.

**Roadmap:** scripted VM bootstrap (`setup-capture-vm`), scripted proxy flags (`networksetup`), provider-supplied WG/OpenVPN configs for parity tunnel tests **without GUI** where allowed.

---

## Nord / Express / Mullvad playbook

- **One UTM VM + one `configs/vpns/<slug>.yaml`** per competitor; rerun `vpn-leaks run ...` per exit geography.
- **Same `surface_urls` pages** (`home`, pricing, signup, portal, checkout, support) wherever possible—diffs then reflect provider behavior rather than methodology drift.

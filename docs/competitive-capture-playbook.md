# Competitive capture playbook

Two-command operator flow: **`capture start`** before signup/install, then **`vpn-leaks run --attach-capture`** on-VPN to run the full harness, stop capture, summarize PCAP, and merge into reports. **No Wireshark** (including `tshark`).

## Implementation backlog

- **vpn-leaks-capture-design:** Session-aware CLI—`capture start` (tcpdump + JSON session desc), `run --attach-capture` finalizes one PCAP spanning signup+install+bench; `capture status|abort`; move pcap from cache to `runs/<id>/raw/.../capture/`.
- **define-artifacts:** Per-provider artifact dirs: `runs/`, research transcripts, optional PCAP/MITM exports, report outputs.
- **utm-vm-per-provider:** UTM baseline image + clone workflow; host prep checklist.
- **capture-stack:** tcpdump filter/rotation; mitmproxy scripting; no Wireshark anywhere.
- **pcap-summarize-report:** Post-run PCAP parser (Python only—dpkt/scapy/custom TLS ClientHello)—`pcap_summary.json`; merge into `normalized.json` + MD/HTML report tables; optional JA fingerprints.
- **yaml-parity:** Nord/Express/Mullvad `surface_urls` / `competitor_probe` / `policy_urls` parity in `configs/vpns/`.
- **ja-fingerprint-toolchain:** JA3/JA4 from ClientHello in summarizer (or vetted non-Wireshark helper); pin versions for comparability.
- **docs:** Keep [website-exposure-methodology.md](website-exposure-methodology.md) authoritative for manual DNS/email supply-chain phases 8–9; align report copy with this playbook.

---

## Repo strategy—capture lives in vpn-leaks

**This repo is the single canonical codebase** for competitive evaluation: `runs/`, `normalized.json`, HAR/`surface_probe`, `competitor_probe`, reports, `graph-export`, and (planned) PCAP session + summarization.

**Authoritative companion docs:** [HANDOFF.md](../HANDOFF.md) (repo map, CLI, artifacts), [website-exposure-methodology.md](website-exposure-methodology.md) (website + DNS infrastructure desk methodology), [methodology.md](methodology.md), [data-dictionary.md](data-dictionary.md).

### What “capture as part of vpn-leaks” means (concrete integrations)

**Primary operator UX (two commands per campaign):**

1. **`vpn-leaks capture start`** (exact name negotiable, e.g. `capture begin`) — **one command** that spawns **long-lived `tcpdump`** on the chosen interface, writes a **session descriptor** (JSON: `session_id`, `pid`, `pcap_path` still growing, `interface`, `started_at_utc`, optional `bpf`). PCAP lives under a **temp/cache dir** until finalized because **`run_id` does not exist yet**. Document **`sudo`** behavior up front.
2. **Human window** — browser signup, download/install vendor app, connect VPN (all traffic **including pre-VPN marketing + installer callbacks** lands in the same PCAP).
3. **`vpn-leaks run --provider <slug> --skip-vpn --attach-capture`** — **second command**: runs the **full existing harness** (leak tests, `competitor_probe`, `surface_urls`, policy, yourinfo, attribution, …) **while tunnel is up**. On **exit** (success or controlled failure): **stop tcpdump** from the active session descriptor, **rotate/close** the PCAP, **move or hardlink** it into `runs/<run_id>/raw/<location_id>/capture/*.pcap`, invoke **`pcap_summary`**, merge into **`normalized.json`**, then teardown session file. If **no** active capture, `run` behaves exactly as today.

**Helpers:** `vpn-leaks capture status` (show active session + bytes written), `vpn-leaks capture abort` (kill tcpdump, discard or quarantine partial pcap), optional `--capture-interface en0` on **start** / default from env.

**Alternate / advanced:** `vpn-leaks run --with-pcap` that **only** wraps the harness window (no signup traffic)—kept for quick retests; not the default story for competitive campaigns.

**Other wrappers:** optional `vpn-leaks capture mitm-run` / mitmdump recipe for decrypted HTTP(S) where CA trust exists—orthogonal to the two-command PCAP story.

- **Run integration (legacy / short capture):** optional flags that **start tcpdump immediately before phases and stop after**—superseded for full-funnel research by **session capture** above.
- **Post-run PCAP review (mandatory design goal):** A **vpn-leaks internal module** parses each saved `.pcap` (Python-only stack—e.g. **dpkt** and/or **scapy-lite path**, custom TLS ClientHello parser for **SNI**/cipher lists, optional JA3/JA4 math from raw hello bytes). **Do not depend on Wireshark** (no GUI, **`tshark` excluded** policy). Outputs **`pcap_summary.json`** beside the PCAP with: aggregated flows (5-tuples + byte/packet counts), top remote IPs/hostnames inferred from TLS SNI / cleartext DNS (`udp/53`, `tcp/53`), optional QUIC heuristic notes, pinning gaps called out explicitly (“opaque TLS to X without SNI”).
- **Report fusion:** Extend **`normalized.json`** (or sibling artifact referenced from it with stable schema) plus **Jinja** templates so `vpn-leaks report` emits a **PCAP-derived exposure** subsection per location in **`VPNs/<SLUG>.md`** and **`VPNs/<SLUG>.html`** (tables + badges: third-party IPs, inferred services, parity with HAR lists). Optional **graph-export** nodes for high-volume third-party edges.
- **This playbook** (and future tight cross-links in README) documents bpf defaults, “no Wireshark” policy, and interpretive limits (encrypted DNS, ESNI/ECH blindness).
- **Dependencies:** PCAP parsing deps live in **`pyproject.toml` extras** (`pcap`, etc.); **`mitmproxy` remains optional/Homebrew**. **Never** Wireshark/mitmshark/tshark.

**Out of scope for bundling:** Proxyman is GUI-first—document it as manual export into `runs/.../capture/proxyman/` rather than automate its binary.

---

## What the output is (files and reports you keep)

You end up with **repeatable evidence bundles per provider** and **rollups**, not a single vague “analysis.”

**Delivered today by vpn-leaks** (per [HANDOFF.md](../HANDOFF.md)); capture features above **extend** this tree—in place—not a second product:

- **Per run folder** `runs/<run_id>/` with `normalized.json` (canonical machine-readable record), `summary.md`, and `raw/<location_id>/` artifacts: IP/DNS/WebRTC/IPv6 checks, attribution (RIPEstat / Team Cymru / PeeringDB), privacy policy fetch + hash, optional **yourinfo.ai** HAR/snapshot, **competitor_probe** (DNS of declared domains, portal HTTPS checks, transit probes, stray JSON), **surface_probe** HARs + `har_summary.json` when you list `surface_urls` in the provider YAML.
- **Rollup after one or more runs:** `vpn-leaks report --provider <slug>` → **`VPNs/<SLUG>.md`** and **`VPNs/<SLUG>.html`** (dashboard + Website/DNS surface section + embedded 3D graph when data exists).
- **Graph export:** `vpn-leaks graph-export --provider <slug> -o exposure-graph.json` → feed [viewer/](../viewer/).

**Desk methodology (DNS/email supply chain Phases 8–9):** [docs/website-exposure-methodology.md](website-exposure-methodology.md). Archive deep transcripts as `runs/.../raw/.../dns-audit-<date>.txt` or under `research/` in this repo.

**Capture extensions to implement** (manual or partial today):

- **Raw PCAP** via **`tcpdump` only** (no Wireshark family); **automatic summarization** post-run proves **which IPs/ports** and inferred identities (SNI/DNS).
- **MITM artifacts** (mitmproxy first-class; Proxyman via manual export): decrypted **HTTP(S)** where pinning allows—stored under `runs/.../raw/.../capture/`.
- **Run metadata:** record harness version, git SHA, interface name, and hostname in **`run.json`** where possible; optionally append tester geography in freeform run notes when CDN POP context matters.

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
brew install python@3.12 git jq mitmproxy
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
which mitmdump tcpdump python3.12
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

No extra **brew** packages required until **vpn-leaks** ships `pcap` extras—then on golden (or first clone after release): **`pip install -e ".[dev,pcap]"`** (exact extra name TBD in implementation). Still **no Wireshark**.

**Not globally required:** Proxyman (GUI MITM)—install only if an analyst wants it; not part of golden minimal path.

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

8. **Optional app MITM / Proxyman** — manual side-channel if you need decrypted bodies where CA trust works; PCAP from steps 5–7 remains the ground truth for metadata.
9. **More cities:** **Command 1** again (or new clone) → reconnect elsewhere → **Command 2** again.
10. **Publishing:** `git` add/commit `runs/`, lift artifacts off the VM as needed.
11. **Executive wording** (“who can see what”)—human reviewer; may draft from normalized outputs.

### Automated by vpn-leaks + capture extensions

Including: **session-scoped PCAP** spanning signup through benchmark; competitor DNS probing; **`surface_urls` Playwright** + **HAR summaries**; leak URLs; **yourinfo.ai** if enabled; **policy** fetch; RIPEstat / Cymru / PeeringDB attribution; **`pcap_summary` + report fusion**; **`vpn-leaks report`** + **`graph-export`**; optional **mitmdump** exporter; JA fingerprints from summarizer.

**Rare escape hatch:** one **manual Safari** capture if Cloudflare defeats Playwright—drop HAR under `runs/.../manual/` and annotate.

---

## Implementer mapping (phases aligned with codebase)

Treat each competitor as multiple **`runs/`** (`location_id`/exit-dependent). Rough mapping:

- **Phase 0:** UTM template + toolchain bootstrap (checklist steps 1–3 above).
- **Phase A:** `capture start` — long-lived PCAP (minus sudo password).
- **Phase B:** Human signup/install/connect — **PCAP includes marketing + installers + tunnel bring-up**.
- **Phase C:** `run --attach-capture` — harness phases + **`capture finalize`** inside same process.
- **Phase D:** Optional MITM pass (**mixed**).

---

## tcpdump vs Proxyman vs mitmproxy

- **tcpdump:** captures **all** IP packets—ports, flows, timing. **Interpretation:** **vpn-leaks post-run PCAP module** parses locally (SNI/DNS aggregates, fingerprints)—**never** through Wireshark/`tshark`. **Limit:** no decrypted HTTP bodies without MITM; ECH/DoH blind spots must be labeled in `pcap_summary.json`.
- **mitmproxy:** decrypted **HTTP(S)** when apps trust your CA; **scriptable** via `mitmdump`. **Limit:** pinning blocks sessions; some control-plane traffic bypasses system HTTP proxy.
- **Proxyman:** same MITM class, strong GUI triage; **manual** export path into run folder—not required for headless benchmarks.

**Practical stack:**

- **Prefer session tcpdump from `capture start` through `run --attach-capture`** so signup/install traffic is captured; optionally add a harness-only BPF if you split sessions later.
- **Run mitmproxy** when you care about **JSON telemetry bodies** and third-party SDK domains from the **app**—accept **partial** coverage.
- **Use Proxyman** when a human needs to **click through** pinning failures and export single flows quickly.

**JA3 / JA4:** Produced by the **`pcap_summary` pipeline** (and mitm TLS metadata when MITM succeeds), not manual tools.

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

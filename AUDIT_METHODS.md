# Audit Methods — a reusable catalog for finding & fixing bugs

A portable playbook of **distinct auditing methods**, each of which finds a *different class* of bug.
Drop this file into any repo. When you want a pass, tell your AI assistant (or yourself) **which method to
run by name** — e.g. *"Run the Multi-Lens Parallel Audit (M1) on this repo,"* or *"Run the Concurrency &
Resource Audit (M5) on the transport layer."*

> **Why a catalog, not one script:** a single audit — however thorough — only reads the code one way and
> catches one slice of bugs. The reliable way to drive the bug count toward zero is to attack the code from
> **several independent angles**, because each method surfaces bugs the others structurally cannot. Two
> thorough static passes of the same code will still miss what a fuzzer, an oracle diff, or an hour of real
> use would catch in minutes.

---

## The one rule (non-negotiable)

> **Every bug found — by any method below — gets a regression test before you move on.**

A fix without a test can silently come back. A fix *with* a test stays dead. This single discipline is what
makes the count trend **down** instead of oscillating. When a test you write to reproduce a bug *passes*
unexpectedly, the bug is elsewhere — keep the test (it documents intent) and keep looking.

Corollary rules:
- **Verify before you fix.** A finding is a *hypothesis* until you've traced the real code path or produced
  a concrete failing input. Adversarially try to *refute* each finding first — audits produce false
  positives, and a wrong "fix" adds risk for no gain.
- **No silent caps.** If a pass bounds its own coverage (top-N, sampled, one module), say so — don't let
  "I looked" read as "it's clean."
- **Keep a ledger.** Log every finding (fixed or deferred) in the Findings Ledger at the bottom so status
  stays truthful across sessions.

---

## Project hooks — fill this in once per repo

The methods reference these. Fill them in (or tell your assistant to detect them) so a pass is concrete.
**When you copy this file into another repo, replace this one table with that repo's values.**

| Hook | This repo (FieldCommand IMS) |
|---|---|
| **Languages / stack** | Raspberry Pi appliance — **HTML/JS** front-end (`html/`), **Python** back-end (`python/`), **bash** setup scripts, systemd/udev units |
| **Build command** | none (no compile). Lint instead: `python -m py_compile python/*.py`, `bash -n scripts/*.sh` |
| **Test command** | _(confirm — a testing runbook exists at `docs_generators/gen_testing_runbook.py`; add `pytest` for the Python back-end)_ |
| **Coverage command** | `pytest --cov` (once tests exist) |
| **Static-analysis / lint** | `ruff`/`flake8` + `mypy` (Python); `eslint` (JS); `shellcheck` + `bash -n` (scripts) |
| **Run / launch the app** | on the Pi via the systemd services / the one-command setup script; front-end pages are `html/*.html` |
| **Input-parsing surfaces** (fuzz targets) | the Python HTTP/API handlers, AMPR/APRS-gate parsing (`amprgate_*.py`), any file/DB importers |
| **Reference oracle** | _(domain-specific — e.g. ICS/NIMS form field definitions if generating ICS forms)_ |
| **Concurrency hot spots** | Python service loops / pollers (`amprgate_poll.py`, `amprgate_status.py`), any threaded background tasks |
| **Security-sensitive surfaces** | **every served HTML page built from data → XSS** (escape all interpolation); the Python web endpoints (injection, path traversal, auth); the callsign / amateur-radio gating; subprocess calls in scripts |
| **Canonical spec / docs to check against** | ICS-NIMS references; `docs/`; add a minimum-hardware-requirements tier (discussion backlog item) |
| **Known-latent list** | _(track in `docs/` or GitHub issues)_ |

---

## Method catalog (ordered by bug-yield per unit of effort)

Each method: **Finds** · **Best for** · **How to run** · **Invoke by saying** · **Effort**.

### Tier 0 — Always-on (set up once, then they run forever)

#### M0 · Static analysis & the zero-warning gate
- **Finds:** null-derefs, undisposed resources, bad async, unreachable code, dead stores, type errors,
  culture-sensitive formatting bugs — whole *classes*, for free, on every build.
- **Best for:** any codebase; do this first, it's the cheapest ROI.
- **How to run:** turn analyzers/linters/type-checkers on at a meaningful level and make them part of the
  build. Curate the noise (silence purely stylistic rules in config) so the *real* warnings surface instead
  of drowning. Then triage every remaining warning — several are usually real bugs.
- **Invoke by saying:** *"Elevate static analysis and clear the warning backlog."*
- **Effort:** Low. One-time setup + a triage pass.

#### M0b · Dependency & secret scan
- **Finds:** known-vulnerable dependencies; secrets/keys accidentally committed.
- **How to run:** a vuln scanner (`dotnet list package --vulnerable`, `npm audit`, `pip-audit`) + a secret
  scan (e.g. `gitleaks`) over the history.
- **Invoke by saying:** *"Run a dependency and secret scan."*
- **Effort:** Low.

### Tier 1 — High-yield audits (run per release, or on demand)

#### M1 · Multi-Lens Parallel Expert Audit  ⭐ the flagship
- **Finds:** the broadest set — correctness, concurrency, resource, security, spec, reachability — because
  several *specialized* reviewers each read the whole codebase through **one lens** and go deep instead of
  broad-and-shallow.
- **Best for:** any substantial codebase; the highest-value single thing you can ask for.
- **How to run:** spin up **independent reviewers in parallel**, one per lens. A good default set:
  1. **Concurrency & resource lifecycle** — shared mutable state, locks across awaits, UI-thread marshaling,
     leaks (undisposed, unbounded growth, event-subscription leaks).
  2. **Correctness / feature logic** — off-by-one, unit/sign/rounding errors, boundary & rollover, state
     machines that can wedge, culture/timezone bugs. *Work a concrete example by hand to prove each.*
  3. **Security** — taint from every source (network/file/user/config) to every sink; auth; injection;
     SSRF; path traversal; secrets; deserialization.
  4. **Domain / spec conformance** — the code vs. the authoritative spec, field by field.
  5. **Resource & API surface** — public API misuse, error handling, disposal contracts, input validation.
  6. **UI / persistence / test quality** — data-binding correctness, reachability, round-trip/corruption
     tolerance, and *weak tests* (assert too little, no coverage of error paths, flaky-by-construction).
  - Give each reviewer: the scope, the rule to **cite `file:line` and give a concrete failure scenario**,
    and a **read-only, verify-don't-speculate** constraint. Then **adversarially verify** every finding
    (spawn skeptics that try to *refute* it) before you fix — kill the false positives.
- **Invoke by saying:** *"Run the Multi-Lens Parallel Audit — fan out the lenses, verify each finding, then
  fix the confirmed ones with regression tests."*
- **Effort:** Medium–High. The best return of any method here.

#### M2 · Oracle / Differential Audit
- **Finds:** subtle correctness bugs in any code with a *known-right answer* — parsers, encoders, format/
  protocol code, calculators, converters, anything with a reference implementation or a spec vector set.
- **Best for:** parsing/serialization/protocol/compatibility/math code. Turns *"I think it's correct"* into
  *"N discrepancies over M inputs."*
- **How to run:** run a **corpus** (real captured data if you have it, else spec examples + edge cases)
  through **both** your code and a **reference oracle** (a second implementation, a trusted library, or
  hand-computed spec answers), and **diff the output field-by-field**. Every mismatch is a candidate bug —
  then decide which side is right per the spec. Grow the corpus over time.
- **Invoke by saying:** *"Run an Oracle Diff of the parser/encoder against <reference> over a broad corpus."*
- **Effort:** Medium (need a corpus + a reference). Very high signal where it applies.

#### M3 · Deterministic Fuzzing (in CI)
- **Finds:** crashes and hangs on malformed/hostile/truncated input that no human would type.
- **Best for:** every input-parsing surface — parsers, codecs, importers, request/body handlers.
- **How to run:** a **seeded** (reproducible) fuzzer that throws hundreds of thousands of random + mutated +
  truncated inputs at *every* parse entry point and asserts **no throw, no hang** (bound it with a time
  budget). Put it **in the test suite** so it runs in CI — a fuzzer that only runs by hand rarely runs.
  Seed the mutation corpus with real, structurally-valid samples so it explores real branches.
- **Invoke by saying:** *"Add/run an in-CI deterministic fuzzer over every parsing surface."*
- **Effort:** Low–Medium. Cheap insurance against a whole crash class.

#### M4 · Property-Based & Round-Trip Testing
- **Finds:** invariant violations and asymmetries between paired operations (encode/decode,
  serialize/parse, compress/expand, save/load).
- **Best for:** anything with an inverse or an invariant ("parsing the thing I generated yields the thing").
- **How to run:** for every emitter, assert **generate → parse → equal**. For invariants, generate random
  valid inputs and assert the property holds (e.g. "sorted output is a permutation of input"). These catch
  bugs that example-based tests miss because they explore the input space, not one hand-picked case.
- **Invoke by saying:** *"Add round-trip / property tests for <X>."*
- **Effort:** Low–Medium.

#### M5 · Concurrency & Resource Audit
- **Finds:** data races, deadlocks, torn reads, UI-thread violations, and leaks — bugs that don't appear in
  normal use, then bite in the field.
- **Best for:** anything with threads, async, background loops, shared caches, or transports.
- **How to run:** three sub-passes —
  1. **Race hunt (review):** find shared mutable state touched from >1 thread with no synchronization;
     collection mutated while enumerated; check-then-act that isn't atomic; UI-bound collections mutated off
     the UI thread; locks held across `await`.
  2. **Stress test:** hammer the shared component from many threads for a bounded window; assert no
     exception (a crash-detection test).
  3. **Lock-ordering / deadlock sweep:** list every lock and the order locks are acquired; flag any two
     paths that take the same pair in opposite orders. **Do this whenever you've *added* locks.**
  - Plus a **leak review:** every `IDisposable`/`Closeable`/timer/CTS/subscription disposed; nothing grows
    without bound over a long session.
- **Invoke by saying:** *"Run the Concurrency & Resource Audit (race hunt + stress + lock-ordering + leaks)."*
- **Effort:** Medium. High-consequence bugs.

#### M6 · Security Taint Audit
- **Finds:** injection (SQL/command/XSS/CSV-formula), SSRF, path traversal, auth bypass / fail-open, secrets
  in logs or URLs, unsafe deserialization, missing security headers, regex-DoS.
- **Best for:** any app with a server, auth, file I/O, outbound HTTP, or subprocess launches.
- **How to run:** for each **source** of untrusted data (network, file, user input, config, packet), trace
  it to every **sink** (HTML/JS, SQL, shell, filesystem path, HTTP request, deserializer) and prove it's
  neutralized. Verify auth is **fail-closed** and comparisons are constant-time. Confirm no code path lets a
  read-only/exercise/replay mode perform a real side effect.
- **Invoke by saying:** *"Run a Security Taint Audit — source-to-sink on every untrusted input."*
- **Effort:** Medium.

#### M7 · Reachability & Dead-Code Audit
- **Finds:** features that are built and wired but **unreachable** (no menu/route/command opens them);
  dead code; commands bound to missing handlers; whole subsystems never called by the live path.
- **Best for:** apps with UI, menus, routes, command palettes, or plugin surfaces.
- **How to run:** from every entry point (menu item, route, CLI command, event subscription), trace to a
  live handler; list anything built but never reached. A compiler/linter won't catch an *orphaned feature* —
  it compiles fine, it's just invisible. Add a test that asserts every command/route resolves.
- **Invoke by saying:** *"Run a Reachability Audit — is every feature actually reachable, and is anything
  orphaned or dead?"*
- **Effort:** Low–Medium. (This class hides from every static tool.)

#### M8 · Coverage-Gap Attack
- **Finds:** untested error paths, reconnect/failover logic, and boundary handling — where bugs concentrate.
- **How to run:** run a coverage report; ignore the happy-path lines; go straight to the **uncovered**
  branches (error handling, retries, timeouts, edge cases) and write tests that exercise them. The
  uncovered lines *are* the risk map.
- **Invoke by saying:** *"Run a Coverage-Gap Attack — test the uncovered error/reconnect/boundary paths."*
- **Effort:** Low–Medium.

#### M9 · Docs / Spec Drift Audit
- **Finds:** behavior that contradicts the docs/manual/spec/comments — either a code bug or a doc lie; both
  matter.
- **How to run:** read the authoritative spec / user manual / API contract next to the code and flag every
  divergence (a shortcut the manual claims but the code doesn't bind; a menu item the code has but the docs
  omit; a comment that describes old behavior). Fix whichever is wrong.
- **Invoke by saying:** *"Run a Docs/Spec Drift Audit."*
- **Effort:** Low–Medium.

### Tier 2 — Real-world methods (need running, time, or hardware)

#### M10 · Human Click-Through / Feature Walkthrough
- **Finds:** the UI/rendering/interaction class that code-reading and unit tests structurally **cannot** —
  layout breakage, a control that does nothing, a dialog that throws on open, a wrong default.
- **How to run:** deliberately open **every** window/screen and exercise **every** feature once, against a
  written checklist — not random poking. This is the single highest-yield thing to do before a release.
- **Invoke by saying:** *"Walk me through a full click-through checklist,"* or drive it with an app-runner /
  browser-automation tool if available.
- **Effort:** Medium (manual), but irreplaceable.

#### M11 · Soak / Leak Test
- **Finds:** slow memory/handle/CPU growth and degradation that only appears after hours of runtime.
- **How to run:** run the app under realistic load for hours; watch memory, handle count, CPU. A flat line
  is a pass; a slope is a leak.
- **Invoke by saying:** *"Set up a soak test and watch for leaks."*
- **Effort:** Medium (mostly waiting).

#### M12 · Real-Endpoint / Fault-Injection
- **Finds:** integration bugs under partial reads, dropped connections, timeouts, and malformed/hostile
  responses from the other side.
- **How to run:** point the integration at a real (or faked) endpoint and inject faults — cut the
  connection mid-stream, return truncated/garbage payloads, stall responses — and confirm graceful
  degradation (no crash, no hang, correct reconnect).
- **Invoke by saying:** *"Run fault-injection against the <integration>."*
- **Effort:** Medium.

---

## How to pick methods for a given codebase

| If the code has… | Run, in order |
|---|---|
| **A parser / encoder / protocol / format** | M2 (oracle), M3 (fuzz), M4 (round-trip), then M1 |
| **Threads / async / transports / schedulers** | M5 (concurrency), M1, then M11 (soak) |
| **A UI (desktop/web/TUI)** | M7 (reachability), M1, M10 (click-through) |
| **A server / auth / file I/O / outbound HTTP** | M6 (security), M12 (fault-injection), M1 |
| **Business/domain logic with a spec** | M9 (spec drift), M2 if a reference exists, M1 |
| **Anything, before a release** | M0 → M1 → M8 → M10 |

You don't run all twelve every time. **Pick the two or three whose bug-class your code actually has**, plus
M1 as the general net. Rotate methods across sessions — a method you ran last time has diminishing returns
this time; a method you *haven't* run is where the next bugs are.

---

## Per-session workflow

1. **Baseline green.** Run the test suite; confirm it passes *before* changing anything.
2. **Pick the method(s)** for this session (see the table). State which at the top — don't scatter.
3. **Hunt.** For each finding: verify it (trace the path or reproduce it) → **write a failing test (red)** →
   fix the smallest thing (green) → confirm the whole suite is still green → commit with a message that
   names the bug and root cause.
4. **Adversarially verify** anything you're not certain of before you fix it. Kill false positives.
5. **Log** every finding — fixed or deferred — in the ledger below.
6. **Update** whatever plan/spec/doc the fixes touched so status stays truthful.

---

## Findings ledger

Keep this current. Status: ☑ fixed · ◐ partial · ☐ open · ⏸ won't-fix (with reason).

| Date | Method | Severity | File:line | Finding | Status |
|---|---|---|---|---|---|
| | | | | | |

---

*This is a method catalog, not a script — don't run it top-to-bottom. Consult it, pick a lane, go deep, and
close every finding with a test. Copy this file into each repo and fill in the Project Hooks table.*

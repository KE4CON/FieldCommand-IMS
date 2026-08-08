# docs/internal — private / local-only documents

**This folder is intentionally kept out of the public repository.** Only this
README is tracked in git; everything else here is git-ignored and is **never
committed or pushed** to the public GitHub remote.

## What lives here

| Category | Files |
|---|---|
| **Org-specific (ESV) editions** — name the real organization | `FieldCommand_ESV_Installation_Guide.pdf`, `FieldCommand_Complete_User_Manual_ESV_v1.0.pdf`, `McHenry_County_RACES_ARES_Starcom_FieldCommand_User_Guide.pdf`, `ESV_Beta_Test_Checklist.pdf`, `ESV_Winlink_Import_Validation_Checklist.pdf`, `ESV_Operator_Access_Cards_DEMO.pdf`, `ESV_IC7300_VARA_Reference_Card.pdf` |
| **Business / financial** | `FieldCommand_ARDC_Grant_Proposal.pdf`, `FieldCommand_Price_Verification.pdf`, `FieldCommand_Tax_Shipping.pdf` |
| **Developer / internal** | `AUDIT_FINDINGS.md`, `MANUAL_VS_CODE.md`, `FieldCommand_Testing_Runbook.pdf`, `ESV_Remaining_Work_Checklist.pdf` |

The **public** editions (generic "World" install guide, user manual, user guide,
quick reference, overview, BOMs, beta package) live in `docs/guides/`,
`docs/hardware/`, and `docs/beta/` and are tracked normally.

## How documents get here

The PDF generators in `docs_generators/` route their output by edition:

- **Public / generic** → `docs/guides` · `docs/hardware` · `docs/beta`
- **ESV / business / dev** → **`docs/internal`** (this folder)

So regenerating any private document lands it here automatically. The
`.gitignore` rule (`docs/internal/*`) is the backstop: **anything placed in this
folder stays private**, even if a generator were ever pointed here by mistake.

Generators that write here: `gen_esv_install_guide.py`, `manual_build.py` (ESV
edition), `gen_user_guide.py` (ESV/McHenry edition), `beta_checklist_build.py`,
`gen_testing_runbook.py`, `price_verification.py`, `tax_shipping_build.py`.

## Important: these files are NOT synced by the public repo

Because this folder is git-ignored, its contents exist **only on the machine
where they were created**. They do **not** travel through the public repo:

- Cloning or pulling the public repo will **not** bring these files down.
- If you build on multiple machines, each machine has its own local copy (or
  none). Back up this folder before wiping a machine.

## Optional: sync these privately across your machines

Pick whichever fits — both keep the docs out of the public repo:

### A. Separate PRIVATE git repo (recommended for versioning)
1. On github.com, create a new **private** repo, e.g. `FieldCommand-IMS-internal`
   (empty — no README).
2. On this machine, from inside this folder:
   ```bash
   cd docs/internal
   git init
   git add .
   git commit -m "Private FieldCommand docs"
   git branch -M main
   git remote add origin https://github.com/KE4CON/FieldCommand-IMS-internal.git
   git push -u origin main
   ```
   (The outer public repo ignores this folder, so this inner repo is completely
   separate. In GitHub Desktop you can add it as a second repository.)
3. On another machine, `git clone` that private repo into `docs/internal/`.

### B. Cloud-synced folder (simplest, no git)
Keep the real files in a private cloud folder (OneDrive / iCloud Drive /
Dropbox / Proton Drive) and point `docs/internal` at it — e.g. move the files
there and create a link/junction named `docs/internal`. Every machine with that
cloud folder then shares the same private docs.

## Never do
- Do not `git add -f` these files into the **public** repo.
- Do not remove the `docs/internal/*` / `!docs/internal/README.md` lines from the
  top-level `.gitignore`.

> Note: files that were committed **before** this folder was made private still
> exist in the public repo's git **history**. Untracking stops future exposure
> only; a full history purge (`git filter-repo` + force-push) is a separate step.

# Drop-in template packs

This folder is how new **incident/event templates** get shipped with FieldCommand
without hand-editing Python.

## How to add a template to a release

1. On a running server, open the **Event Templates** page, build (or refine) the
   template, and tick **"Suggest this template for future FieldCommand updates" (⤴)**,
   then save it.
2. Click **"⤴ Export Update Candidates"** in the toolbar. You get a file named
   `fieldcommand-update-candidates-YYYY-MM-DD.json`.
3. Review it, give it a clear name (e.g. `wildland-fire-pack.json`), and **drop it
   into this folder.** Commit it. That's the whole job — no code to edit.

The file is just JSON: one template object, or an array of them, in the same shape
the Event Templates page exports (`id, name, icon, type, summary, sort_order,
is_builtin, enabled, data`). A `data.propose_upstream` flag, if present, is ignored
on load.

## What the loader does (and deliberately does not do)

`load_template_packs()` in `db.py` runs on **every** startup and, for each template
in every `*.json` here:

- **Adds it only if its `id` is not already in the database.** New templates appear
  — including on field servers that are just being updated, not only fresh installs.
- **Never overwrites an existing template.** The original built-ins and any local
  edits an operator has made are always left exactly as they are. If you need to push
  a *corrected* version of an already-shipped template, give it a **new `id`** (that
  is a deliberate change, not an accident waiting to happen).
- Marks loaded templates as **built-in** (`is_builtin=1`): they show with the
  standard set and are protected from deletion, but stay fully editable/disable-able.
- Skips any malformed file with a log warning — a bad pack never stops startup.

## Rules of thumb

- Keep each `id` **unique and stable**. Reusing an id from the built-in set means the
  pack entry is skipped (the built-in wins).
- Prefer short, descriptive filenames grouped by theme (`shelter-ops.json`,
  `hazmat.json`) over one giant file — easier to review in a diff.
- These are **public/World-safe** templates. Do not put org-specific or private
  content here; that belongs in an agency's own local templates, not the shipped set.

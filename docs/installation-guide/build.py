"""
FieldCommand IMS Installation Guide — edition-aware builder (Word / house pipeline).

One source, two editions. Chapter text uses {{token}} placeholders; this builder substitutes the
tokens for each edition (World = generic public-service; ESV = McHenry County ESV) and emits, per
edition, a Markdown source of truth plus a styled .docx (navy+gold house style, matching the User
Manual and Programming Guide). Chapters are validated JSON under ./chapters/*.json using the shared
block schema (h1/h2/p/steps/bullets/callout/code/table). The Installation Guide carries NO
screenshots by design.

Tokens are shared with the User Manual: the World values live in ../user-manual/editions.json and the
private ESV values in ../internal/editions_esv.json (gitignored). Both are loaded here so there is a
single source of truth for edition wording across every FieldCommand document.

Run:  python build.py                 -> builds BOTH editions
      python build.py World|ESV       -> builds one edition
Env:  INSTALL_OUT overrides the .docx output DIRECTORY (used when Word has a file locked).
"""
import os
import sys
import glob
import json
import re
import datetime

HERE = os.path.dirname(__file__)
# Reuse the shared house style that the User Manual uses (navy+gold, same renderer).
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "user-manual")))
import style as S  # noqa: E402

# ---- editions / tokens (shared with the User Manual) ----------------------
_UM = os.path.abspath(os.path.join(HERE, "..", "user-manual", "editions.json"))
EDITIONS = json.load(open(_UM, encoding="utf-8"))
EDITIONS.pop("_comment", None)
_PRIV = os.path.abspath(os.path.join(HERE, "..", "internal", "editions_esv.json"))
if os.path.exists(_PRIV):
    priv = json.load(open(_PRIV, encoding="utf-8"))
    priv.pop("_comment", None)
    EDITIONS.update(priv)
TODAY = datetime.date.today().strftime("%B %d, %Y")

PUBLIC_DIR = os.path.abspath(os.path.join(HERE, "..", "guides"))      # committed
PRIVATE_DIR = os.path.abspath(os.path.join(HERE, "..", "internal"))   # gitignored


def load_chapters():
    out = []
    for path in sorted(glob.glob(os.path.join(HERE, "chapters", "*.json"))):
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
        ch = raw.get("chapter", raw)
        out.append((int(raw.get("order", ch.get("order", 999))), ch))
    out.sort(key=lambda x: x[0])
    return out


# ---- edition token substitution -------------------------------------------
_TOKEN = re.compile(r"\{\{(\w+)\}\}")


def apply_tokens(obj, tokens):
    """Recursively substitute {{token}} in every string within a chapter dict."""
    if isinstance(obj, str):
        return _TOKEN.sub(lambda m: tokens.get(m.group(1), m.group(0)), obj)
    if isinstance(obj, list):
        return [apply_tokens(x, tokens) for x in obj]
    if isinstance(obj, dict):
        return {k: apply_tokens(v, tokens) for k, v in obj.items()}
    return obj


# ---- Markdown emitter (source of truth) -----------------------------------
def _md_inline(text):
    return re.sub(r"__(.+?)__", r"*\1*", str(text))


def _md_blocks(blocks):
    lines = []
    for blk in blocks:
        if not isinstance(blk, dict):
            continue
        if "h1" in blk:
            lines.append(f"\n## {blk['h1']}\n")
        elif "h2" in blk:
            lines.append(f"\n### {blk['h2']}\n")
        elif "p" in blk:
            lines.append(_md_inline(blk["p"]) + "\n")
        elif "steps" in blk:
            lines += [f"{i}. {_md_inline(s)}" for i, s in enumerate(blk["steps"], 1)]
            lines.append("")
        elif "bullets" in blk:
            lines += [f"- {_md_inline(b)}" for b in blk["bullets"]]
            lines.append("")
        elif "callout" in blk:
            c = blk["callout"] if isinstance(blk["callout"], dict) else {}
            label = c.get("label", c.get("kind", "NOTE").upper())
            lines.append(f"> **{label}** — {_md_inline(c.get('text', ''))}\n")
        elif "screenshot" in blk:
            lines.append(f"> _[Figure: {blk['screenshot']}]_\n")
        elif "code" in blk:
            code = blk["code"]
            code = "\n".join(code) if isinstance(code, list) else str(code)
            lines.append("```\n" + code + "\n```\n")
        elif "table" in blk:
            t = blk["table"] if isinstance(blk["table"], dict) else {}
            headers = [str(h) for h in t.get("headers", [])]
            rows = t.get("rows", [])
            if headers:
                lines.append("| " + " | ".join(headers) + " |")
                lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
                for r in rows:
                    lines.append("| " + " | ".join(_md_inline(c) for c in r) + " |")
                lines.append("")
    return "\n".join(lines)


def to_markdown(chapters, ed_label):
    parts = [
        f"# FieldCommand IMS — Installation Guide ({ed_label})\n",
        "*Set up the field server, the network, the workstations, and the offline data — step by step, in plain language.*\n",
        f"*Generated {TODAY} · Markdown is the living source of truth.*\n",
        "\n---\n",
    ]
    for number, (_o, ch) in enumerate(chapters, 1):
        parts.append(f"\n# {number}. {ch.get('title', 'Untitled')}\n")
        if ch.get("subtitle"):
            parts.append(f"*{_md_inline(ch['subtitle'])}*\n")
        parts.append(_md_blocks(ch.get("blocks", [])))
    return "\n".join(parts)


# ---- styled .docx ---------------------------------------------------------
def build_docx(chapters, ed, out_dir):
    infix = ed.get("infix", "")
    doc = S.new_document(
        header_title=f"FieldCommand IMS — Installation Guide ({ed['label']})",
        header_sub="ICS / NIMS incident management  ·  offline-first field server",
        footer_left="FieldCommand IMS  ·  AGPL v3 (software) / CC BY-SA 4.0 (docs)  ·  KE4CON",
    )
    S.cover(
        doc,
        kicker="FIELDCOMMAND IMS",
        big_title="FieldCommand IMS",
        subtitle="Incident Management System",
        doc_kind="INSTALLATION GUIDE",
        version=f"v1.0  ·  {ed['label']}",
        tagline="Build the offline-first field server from one command — then the network, the workstations, printing, and the offline data library.",
        author="James Rospopo  ·  KE4CON",
        date_str=TODAY,
    )
    S.section_title(doc, "Contents")
    S.toc(doc)
    for number, (_o, ch) in enumerate(chapters, 1):
        S.render_chapter(doc, ch, number)
    out = os.path.join(out_dir, f"FieldCommand_Installation_Guide{infix}.docx")
    doc.save(out)
    return out


def build_edition(chapters_raw, ed_key):
    ed = EDITIONS[ed_key]
    tokens = ed["tokens"]
    chapters = [(o, apply_tokens(ch, tokens)) for o, ch in chapters_raw]
    out_dir = os.environ.get("INSTALL_OUT") or (PRIVATE_DIR if ed.get("private") else PUBLIC_DIR)
    os.makedirs(out_dir, exist_ok=True)
    md = to_markdown(chapters, ed["label"])
    # World Markdown source of truth stays next to the source; ESV Markdown stays private.
    md_dir = out_dir if ed.get("private") else HERE
    md_path = os.path.join(md_dir, f"FieldCommand_Installation_Guide{ed.get('infix','')}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    docx_path = build_docx(chapters, ed, out_dir)
    return md_path, docx_path


def main():
    chapters_raw = load_chapters()
    if not chapters_raw:
        print("No chapters in ./chapters/*.json yet.")
        return
    which = sys.argv[1:] or list(EDITIONS.keys())
    for ed_key in which:
        if ed_key not in EDITIONS:
            print("unknown edition:", ed_key); continue
        md_path, docx_path = build_edition(chapters_raw, ed_key)
        print(f"OK [{ed_key}] - {len(chapters_raw)} chapter(s)")
        print(f"   md:  {md_path}")
        print(f"   docx:{docx_path}")


if __name__ == "__main__":
    main()

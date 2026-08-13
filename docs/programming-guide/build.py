"""
FieldCommand IMS Programming Guide — builder (Word / house pipeline).

A maintainer's code book: What it does -> Why it was built this way -> How it works, grounded in the
real source and quoting exact code excerpts. Single edition (the code is edition-neutral). Markdown is
the living source of truth; a styled .docx (navy+gold house style, matching the User Manual and
Installation Guide) is generated from the same per-chapter JSON under ./chapters/*.json using the shared
block schema (h1/h2/p/steps/bullets/callout/code/table). No screenshots by design (it is a code book).

Run:  python build.py    -> writes ../guides/FieldCommand_Programming_Guide.docx and ./FieldCommand_Programming_Guide.md
Env:  PROG_OUT overrides the .docx output DIRECTORY (used when Word has the file locked).
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

TODAY = datetime.date.today().strftime("%B %d, %Y")
PUBLIC_DIR = os.path.abspath(os.path.join(HERE, "..", "guides"))


def load_chapters():
    out = []
    for path in sorted(glob.glob(os.path.join(HERE, "chapters", "*.json"))):
        with open(path, encoding="utf-8") as f:
            raw = json.load(f)
        ch = raw.get("chapter", raw)
        out.append((int(raw.get("order", ch.get("order", 999))), ch))
    out.sort(key=lambda x: x[0])
    return out


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


def to_markdown(chapters):
    parts = [
        "# FieldCommand IMS — Programming Guide\n",
        "*How the code works, and why — plain enough to follow, deep enough to maintain.*\n",
        f"*Generated {TODAY} · Markdown is the living source of truth.*\n",
        "\n---\n",
    ]
    for number, (_o, ch) in enumerate(chapters, 1):
        parts.append(f"\n# {number}. {ch.get('title', 'Untitled')}\n")
        if ch.get("subtitle"):
            parts.append(f"*{_md_inline(ch['subtitle'])}*\n")
        parts.append(_md_blocks(ch.get("blocks", [])))
    return "\n".join(parts)


def build_docx(chapters, out_dir):
    doc = S.new_document(
        header_title="FieldCommand IMS — Programming Guide",
        header_sub="ICS / NIMS incident management  ·  offline-first  ·  nginx + Python + SQLite",
        footer_left="FieldCommand IMS  ·  AGPL v3 (software) / CC BY-SA 4.0 (docs)  ·  KE4CON",
    )
    S.cover(
        doc,
        kicker="FIELDCOMMAND IMS",
        big_title="FieldCommand IMS",
        subtitle="Incident Management System",
        doc_kind="PROGRAMMING GUIDE",
        version="v1.0",
        tagline="How the offline-first field server is built — the architecture, the Python services, the SQLite data layer, the web front end, and the install & boot chain — What, Why, and How.",
        author="James Rospopo  ·  KE4CON",
        date_str=TODAY,
    )
    S.section_title(doc, "Contents")
    S.toc(doc)
    for number, (_o, ch) in enumerate(chapters, 1):
        S.render_chapter(doc, ch, number)
    out = os.path.join(out_dir, "FieldCommand_Programming_Guide.docx")
    doc.save(out)
    return out


def main():
    chapters = load_chapters()
    if not chapters:
        print("No chapters in ./chapters/*.json yet.")
        return
    md = to_markdown(chapters)
    md_path = os.path.join(HERE, "FieldCommand_Programming_Guide.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    out_dir = os.environ.get("PROG_OUT") or PUBLIC_DIR
    os.makedirs(out_dir, exist_ok=True)
    docx_path = build_docx(chapters, out_dir)
    print(f"OK - {len(chapters)} chapter(s)")
    print(f"   md:  {md_path}")
    print(f"   docx:{docx_path}")


if __name__ == "__main__":
    main()

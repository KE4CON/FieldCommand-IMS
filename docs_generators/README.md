# FieldCommand IMS — Documentation Generators

## CRITICAL — READ THIS FIRST

These Python scripts build all FieldCommand IMS documentation PDFs using ReportLab.
**Generator scripts are NOT persistent between Claude sessions — they live only in the Claude environment.**
**They MUST be committed to GitHub after every editing session or they will be lost.**

---

## Session workflow for Claude

At the end of every session that modifies any generator or PDF:
1. Copy updated generator to `fieldcommand/docs_generators/`
2. Copy updated PDF to `fieldcommand/docs/`
3. Commit and push:
```bash
git add docs_generators/ docs/ && git commit -m "description" && git push
```

If a generator is missing at the start of a session, tell Claude:
> "Rebuild the [document name] generator from the current PDF"

---

## Document inventory

### Grant & Business Documents
| PDF | Generator | Status |
|-----|-----------|--------|
| FieldCommand_ARDC_Grant_Proposal.pdf | ardc_proposal.py | ✓ In repo |
| FieldCommand_Leadership_Brief.pdf | leadership_brief.py | ⚠ Not in repo — rebuild if needed |
| FieldCommand_BOM.pdf | bom_build.py | ✓ In repo |
| FieldCommand_Price_Verification.pdf | price_verification.py | ✓ In repo |
| FieldCommand_Tax_Shipping.pdf | tax_shipping_build.py | ✓ In repo |

### Technical Documents
| PDF | Generator | Status |
|-----|-----------|--------|
| FieldCommand_Installation_Guide.pdf | gen_install_guide.py | ✓ In repo |
| FieldCommand_Complete_User_Manual_v1.0.pdf | manual_build.py + manual_ch_*.py + manual_framework.py | ✓ In repo |
| McHenry_County_RACES_ARES_Starcom_FieldCommand_User_Guide.pdf | gen_user_guide.py | ✓ In repo |
| FieldCommand_Field_Quick_Reference.pdf | gen_field_quickref.py | ✓ In repo |

### Operational Documents
| PDF | Generator | Status |
|-----|-----------|--------|
| ESV_Beta_Test_Checklist.pdf | beta_checklist_build.py | ✓ In repo |
| IncidentManagement_Overview.pdf | overview_build.py | ✓ In repo |

---

## Document style guide

All PDFs follow the FieldCommand IMS cover page pattern:
- Full-page navy EOC fill (`#1a3a6b`)
- Gold accent stripes top and bottom (`#f0c040`)
- FIELDCOMMAND IMS 58pt white centered
- Subtitle gold 15pt
- Gold HR rule
- Document type 28pt white
- Footer: `© 2026 James Rospopo KE4CON · CC BY-SA 4.0 · creativecommons.org/licenses/by-sa/4.0`
- Author metadata: `author='James Rospopo KE4CON'`

## Rebuild dependencies

```bash
pip install reportlab pypdf --break-system-packages
```

## Key patterns

- **CodeBlock:** Each line as separate Table row — see `gen_install_guide.py` CodeBlock() function
- **Table cell wrapping:** All tables need `repeatRows=1`, `splitByRow=1`
- **TOC overflow:** 8.5pt font, 2pt padding — see manual_framework.py
- **ManualCanvas.save() TOTAL fix:** Set `total = len(self._saved)` BEFORE loop
- **CC-BY-SA footer:** On every page of every document — non-negotiable

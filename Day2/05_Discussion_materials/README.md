# Day 2 discussion: supporting files

Updated on 2026-10-09 for the 15:30 discussion (`05_Discussion_trust_and_MEMOTE.pptx`). Open a report in a web browser to show a real MEMOTE report during the session.

## memote_reports/
MEMOTE 0.17.0 snapshot reports (`memote report snapshot --filename report.html model.xml`).
- `iML1515`, `iYO844`, `iNF517`: the curated models from BiGG (`../04_Models/*.xml`).
- `KBase_*`: the instructors' KBase drafts (`../04_Models/*.RAST.mdl.json.zip`, built on 9 October 2026 with
  "MS2 - Build Prokaryotic Metabolic Models"; E. coli and B. subtilis gap-filled on Carbon-D-Glucose, L. lactis on AuxoMedia).
  KBase exports its own JSON format, so each model was converted to SBML with `load_model()` from
  `../04_Compare_with_BiGG/kbase_models.py` before running MEMOTE.

## Two things to know before showing the KBase reports
- **Stoichiometric consistency.** The E. coli and B. subtilis drafts fail this test: 73 and 67 of their reactions do not
  balance protons (KBase's nitrate reductases among them), and together these let the network create or destroy protons.
  With those reactions removed, the test passes. The L. lactis draft has 44 such reactions, but they don't close a loop.
- **Energy-generating cycles.** MEMOTE flags them in all three drafts. They are false alarms: MEMOTE's test resets every
  one-way reaction to run forwards, and the drafts store 61 to 86 reactions as running backwards. With those reactions
  written forwards, the same test finds no cycles, and a direct test finds no ATP made from nothing.

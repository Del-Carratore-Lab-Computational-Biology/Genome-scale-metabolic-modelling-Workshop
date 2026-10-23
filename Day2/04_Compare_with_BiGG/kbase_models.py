"""Helpers for the CODE-M Day 2 comparison notebook.

You do not need to read this file to follow the notebook. It provides:

* load_model(path) - reads a model exported from KBase (the .json or .json.zip from
  "Export / Download data"), an SBML file (.xml/.sbml) or a cobrapy JSON file,
  and returns a cobrapy Model;
* CARBON_D_GLUCOSE, AUXOMEDIA - the two KBase media used on Day 2, as
  {ModelSEED compound id: maximum uptake};
* M9_GLUCOSE_BIGG - the same minimal glucose medium in BiGG identifiers.

KBase stores models in its own format (KBaseFBA.FBAModel), not as cobrapy models.
load_model() converts it: reactions keep their KBase direction and bounds, gene rules
are rebuilt from the protein complexes, and an exchange reaction EX_<compound>_e0 is
added for every extracellular compound, as KBase does when it runs FBA. Reactions
added by gap-filling are marked with reaction.notes["gapfilled"].
"""
import json
import re
import zipfile

import cobra
from cobra import Metabolite, Model, Reaction


# KBaseMedia/Carbon-D-Glucose (ModelSEED Database, Media/media_list_with_meta.txt): maximum uptake per compound
CARBON_D_GLUCOSE = {
    "cpd00027": 5,     # D-glucose
    "cpd00007": 10,    # O2
    "cpd00001": 100, "cpd00009": 100, "cpd00013": 100, "cpd00030": 100, "cpd00034": 100, "cpd00048": 100,
    "cpd00058": 100, "cpd00063": 100, "cpd00067": 100, "cpd00099": 100, "cpd00149": 100, "cpd00205": 100,
    "cpd00244": 100, "cpd00254": 100, "cpd00971": 100, "cpd10515": 100, "cpd10516": 100, "cpd11574": 100,
}
# AuxoMedia is glucose plus all amino acids, vitamins and other common growth factors. Its exact recipe is not in
# the model export; this approximation adds to Carbon-D-Glucose the 20 amino acids, 8 B vitamins, heme, the
# polyamines putrescine and spermidine, and the bases adenine, guanine and uracil. (The L. lactis model gap-filled
# on AuxoMedia in KBase needs heme, putrescine and spermidine to grow.)
_AMINO_ACIDS = ["cpd00035", "cpd00051", "cpd00132", "cpd00041", "cpd00084", "cpd00053", "cpd00023", "cpd00033",
                "cpd00119", "cpd00322", "cpd00107", "cpd00039", "cpd00060", "cpd00066", "cpd00129", "cpd00054",
                "cpd00161", "cpd00065", "cpd00069", "cpd00156"]
_VITAMINS = ["cpd00305", "cpd00220", "cpd00218", "cpd00644", "cpd00215", "cpd00104", "cpd00393", "cpd00443"]
_OTHER = ["cpd00028", "cpd00118", "cpd00264", "cpd00128", "cpd00207", "cpd00092"]   # heme, putrescine, spermidine, adenine, guanine, uracil
AUXOMEDIA = {**CARBON_D_GLUCOSE, **{c: 10 for c in _AMINO_ACIDS + _VITAMINS + _OTHER}}

# Minimal glucose medium in BiGG identifiers (M9 salts + glucose)
M9_GLUCOSE_BIGG = {"glc__D": 10, "o2": 1000, **{c: 1000 for c in
                   "ca2 cl cobalt2 cu2 fe2 fe3 h2o h k mg2 mn2 mobd na1 nh4 ni2 pi so4 zn2".split()}}


def _read_kbase_json(path):
    if path.endswith(".zip"):
        with zipfile.ZipFile(path) as zf:
            names = [n for n in zf.namelist() if n.endswith(".json") and "KBase_object_details" not in n]
            if len(names) != 1:
                raise ValueError(f"expected one model .json inside {path}, found {names}")
            return json.loads(zf.read(names[0]))
    with open(path) as fh:
        return json.load(fh)


def _ref_id(ref):
    """'~/modelcompounds/id/cpd00027_e0' -> 'cpd00027_e0'"""
    return ref.rsplit("/", 1)[-1]


def _gpr(protein_list):
    """KBase proteins (OR) -> subunits (AND) -> genes (OR) as a cobrapy gene rule."""
    complexes = []
    for protein in protein_list:
        subunits = []
        required = [s for s in protein.get("modelReactionProteinSubunits", []) if not s.get("optionalSubunit")]
        for su in required or protein.get("modelReactionProteinSubunits", []):
            genes = sorted({_ref_id(f) for f in su.get("feature_refs", [])})
            if genes:
                subunits.append(genes[0] if len(genes) == 1 else "(" + " or ".join(genes) + ")")
        subunits = list(dict.fromkeys(subunits))   # two subunits can map to the same gene
        if subunits:
            complexes.append(subunits[0] if len(subunits) == 1 else "(" + " and ".join(subunits) + ")")
    complexes = sorted(set(complexes))
    return " or ".join(complexes)


def _gapfill_note(gapfill_data):
    """{'Carbon-D-Glucose': {'0': ['>', 1, []]}} -> 'Carbon-D-Glucose (forward)'"""
    words = {">": "forward", "<": "reverse", "=": "both directions"}
    notes = []
    for media, solutions in gapfill_data.items():
        for value in solutions.values():
            notes.append(f"{media} ({words.get(value[0], value[0])})")
    return "; ".join(sorted(set(notes)))


def _clean_name(name):
    return re.sub(r"\s*\[[ce]\d\]$", "", name or "")


def _kbase_to_cobra(data):
    model = Model(data["id"], name=data.get("name"))
    labels = {c["id"]: c.get("label", c["id"]) for c in data["modelcompartments"]}
    model.compartments = labels
    mets = {}
    for c in data["modelcompounds"]:
        comp = _ref_id(c["modelcompartment_ref"])
        mets[c["id"]] = Metabolite(c["id"], formula=c.get("formula") or None, name=_clean_name(c.get("name")),
                                   charge=c.get("charge"), compartment=comp)
    model.add_metabolites(list(mets.values()))
    reactions = []
    for r in data["modelreactions"]:
        d = r.get("direction", "=")
        lb = -float(r.get("maxrevflux", 1000)) if d in "<=" else 0.0
        ub = float(r.get("maxforflux", 1000)) if d in ">=" else 0.0
        rxn = Reaction(r["id"], name=_clean_name(r.get("name")), lower_bound=lb, upper_bound=ub)
        stoich = {}
        for reagent in r["modelReactionReagents"]:
            met = mets[_ref_id(reagent["modelcompound_ref"])]
            stoich[met] = stoich.get(met, 0) + reagent["coefficient"]
        rxn.add_metabolites({m: v for m, v in stoich.items() if v != 0})
        rxn.gene_reaction_rule = _gpr(r.get("modelReactionProteins", []))
        if r.get("gapfill_data"):
            rxn.notes["gapfilled"] = _gapfill_note(r["gapfill_data"])
        reactions.append(rxn)
    for b in data.get("biomasses", []):
        rxn = Reaction(b["id"], name=b.get("name", "biomass"), lower_bound=0, upper_bound=1000)
        rxn.add_metabolites({mets[_ref_id(x["modelcompound_ref"])]: x["coefficient"] for x in b["biomasscompounds"]})
        reactions.append(rxn)
    # Boundary reactions are built directly rather than with model.add_boundary(), which in some cobrapy
    # versions guesses the external compartment and does not recognise KBase's "e0".
    for met in [m for m in mets.values() if m.compartment.startswith("e")]:
        ex = Reaction(f"EX_{met.id}", name=f"{met.name} exchange", lower_bound=0, upper_bound=1000)
        ex.add_metabolites({met: -1})
        ex.annotation["sbo"] = "SBO:0000627"
        reactions.append(ex)
    for cpd, (lb, ub) in (data.get("drain_list") or {}).items():
        if cpd in mets:
            dm = Reaction(f"DM_{cpd}", name=f"{mets[cpd].name} demand", lower_bound=lb, upper_bound=ub)
            dm.add_metabolites({mets[cpd]: -1})
            dm.annotation["sbo"] = "SBO:0000628"
            reactions.append(dm)
    model.add_reactions(reactions)
    if data.get("biomasses"):
        model.objective = data["biomasses"][0]["id"]
    return model


def load_model(path):
    """Read a KBase export (.json / .json.zip), an SBML file or a cobrapy JSON model."""
    path = str(path)
    if path.endswith((".xml", ".sbml")):
        return cobra.io.read_sbml_model(path)
    data = _read_kbase_json(path)
    if "modelreactions" in data:      # KBase FBAModel
        return _kbase_to_cobra(data)
    return cobra.io.load_json_model(path)


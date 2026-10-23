# CODE-M Workshop: Genome-Scale Metabolic Modelling

**Constraint-based & Dynamic models — Exploring Metabolism**

[![Materials: CC BY 4.0](https://img.shields.io/badge/materials-CC%20BY%204.0-lightgrey.svg)](LICENSE)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE-CODE)
[![Python 3.11 | 3.12](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](requirements.txt)

Materials for a three-day, hands-on workshop on genome-scale metabolic models (GSMMs). Day 1 introduces the
concepts and flux balance analysis (FBA). Day 2 shows where models come from: you reconstruct a small bacterium
by hand, then compare automated ModelSEED drafts with curated models. Day 3 puts models to work on flux
variability, gene essentiality, strain design and omics integration. All hands-on work is in Python with
[cobrapy](https://opencobra.github.io/cobrapy/).

This repository contains the slides, the Jupyter notebooks for the hands-on sessions, their helper code, and
every model file the notebooks need.

| Day | Theme | Led by | Main tools |
|---|---|---|---|
| Day 1 | Concepts: systems biology, GSMMs and FBA | Stephen Chapman | cobrapy, Escher |
| Day 2 | Reconstruction: from a toy model to automated pipelines | Francesco Del Carratore | cobrapy, ModelSEED (KBase), MEMOTE |
| Day 3 | Advanced analysis, strain design and omics integration | Francesco Del Carratore and Stephen Chapman | cobrapy |

## Learning outcomes

**Day 1.** By the end of the day you can:
- explain the genome → transcriptome → metabolome relationship and where omics databases (NCBI, PDB, KEGG) fit;
- describe what a GSMM contains and download one as SBML from BiGG;
- state the FBA problem (S·v = 0, flux bounds, objective) and run a first FBA in cobrapy;
- interpret an FBA solution and visualise fluxes on an Escher map.

**Day 2.** By the end of the day you can:
- build a small model from scratch in cobrapy (metabolites, reactions, bounds, GPRs, objective) and save it as SBML;
- explain the stages of a reconstruction pipeline (genome → annotation → draft network → gap-filling → curation);
- build models with ModelSEED and compare them with curated ones.

**Day 3.** By the end of the day you can:
- run pFBA and FVA on a genome-scale model and interpret how they differ from plain FBA;
- identify essential genes and reactions, and use knockouts to redirect flux toward a target product;
- apply a basic omics-integration method to constrain a model to a condition.

## Programme and materials

Sessions are listed in the order they run. The run sheet, with timings and session leads, is
[CODE-M_Run_Sheet.docx](CODE-M_Run_Sheet.docx).

### Day 1: Concepts — systems biology, GSMMs and FBA

| Session | Slides | Notebook and files |
|---|---|---|
| Welcome and aims; the environment–phenotype problem | [0_1_intro.pptx](Day1/0_1_intro.pptx) | |
| Lecture 1: introduction to systems biology; omics data; NCBI, PDB and KEGG | [1_sys_biology.pptx](Day1/1_sys_biology.pptx) | |
| Lecture 2: what is a GSMM? Model contents, downloading SBML from BiGG, introduction to cobrapy | [2_genome_scale_metabolic_models.pptx](Day1/2_genome_scale_metabolic_models.pptx) | [2_1.ipynb](Day1/2_1.ipynb): live demo, loading and exploring a model |
| Lecture 3: flux balance analysis; introduction to FVA; limitations and applications | [2_1_FBA.pptx](Day1/2_1_FBA.pptx) | |
| Hands-on: FBA of *E. coli* on different media, Escher flux maps, and an exercise on ethanol production by *S. cerevisiae* | | [3_1.ipynb](Day1/3_1.ipynb), with [iJO1366.xml](Day1/iJO1366.xml) and [iMM904.xml](Day1/iMM904.xml) |

### Day 2: Reconstruction

| Session | Slides | Notebook and files |
|---|---|---|
| Recap of Day 1; the reconstruction problem | [01_Recap_and_Reconstruction_Problem.pptx](Day2/01_Recap_and_Reconstruction_Problem.pptx) | |
| Hands-on A: reconstruct a fictional bacterium, *Toybacter fermentans*, by hand: annotation, GPRs, exchanges, biomass, quality control, gap-filling and validation | | [Day2_A_Toy_reconstruction_STUDENT.ipynb](Day2/02_Toy_reconstruction/Day2_A_Toy_reconstruction_STUDENT.ipynb) |
| Talk: reconstruction pipelines (annotation, draft networks, gap-filling, curation; CarveMe, ModelSEED, gapseq, KBase) | [03_Reconstruction_pipelines.pptx](Day2/03_Reconstruction_pipelines.pptx) | |
| Hands-on B: build draft models of three bacteria with ModelSEED in KBase, then compare them with their curated BiGG models | [04_ModelSEED_three_bacteria.pptx](Day2/04_ModelSEED_three_bacteria.pptx) | [Day2_B_Compare_with_BiGG_STUDENT.ipynb](Day2/04_Compare_with_BiGG/Day2_B_Compare_with_BiGG_STUDENT.ipynb), with the models in [04_Models/](Day2/04_Models) |
| Discussion: how far can we trust an automated draft? Quality metrics with MEMOTE | [05_Discussion_trust_and_MEMOTE.pptx](Day2/05_Discussion_trust_and_MEMOTE.pptx) | MEMOTE reports in [05_Discussion_materials/](Day2/05_Discussion_materials) |

### Day 3: Advanced analysis, design and omics

| Session | Slides | Notebook and files |
|---|---|---|
| Recap of Days 1 and 2; plan for the day | [01_Recap_and_Day3_plan.pptx](Day3/01_Recap_and_Day3_plan.pptx) | |
| Hands-on A: beyond one FBA solution — alternative optima, FVA, pFBA, robustness and phase planes; yeast with and without oxygen | | [Day3_A_Beyond_FBA_STUDENT.ipynb](Day3/02_Beyond_FBA/Day3_A_Beyond_FBA_STUDENT.ipynb) |
| Hands-on B: gene essentiality, synthetic lethality, production envelopes, and designing a producer strain | | [Day3_B_Essentiality_and_design_STUDENT.ipynb](Day3/03_Essentiality_and_design/Day3_B_Essentiality_and_design_STUDENT.ipynb) |
| Lecture: omics integration — from GPRs to reaction scores; constraint- and objective-based methods (GIMME, iMAT, E-Flux) | [4_data_integration.pptx](Day3/4_data_integration.pptx) | |

Both Day 3 notebooks use the models in [Day3/models/](Day3/models).

## Repository layout

```
.
├── Day1/                            Concepts and FBA
│   ├── *.pptx                       slides
│   ├── 2_1.ipynb                    demo: loading and exploring a model
│   ├── 3_1.ipynb                    hands-on: FBA and Escher maps
│   └── iJO1366.xml, iMM904.xml      models (E. coli, S. cerevisiae)
├── Day2/                            Reconstruction
│   ├── *.pptx                       slides
│   ├── 02_Toy_reconstruction/       hands-on A: notebook, drawing helpers, the toy model and its Escher map
│   ├── 04_Compare_with_BiGG/        hands-on B: notebook, KBase model loader, the scorecard it fills in
│   ├── 04_Models/                   ModelSEED drafts (KBase exports) and curated BiGG models
│   └── 05_Discussion_materials/     MEMOTE reports for the six models (see its README)
├── Day3/                            Advanced analysis and design
│   ├── *.pptx                       slides
│   ├── 02_Beyond_FBA/               hands-on A: notebook and helpers
│   ├── 03_Essentiality_and_design/  hands-on B: notebook and helpers
│   └── models/                      E. coli core (with its Escher map), iML1515, iMM904
├── CODE-M_Run_Sheet.docx            run sheet: schedule, learning aims, session leads
├── requirements.txt                 Python packages (pip)
├── environment.yml                  the same packages as a conda environment
├── CITATION.cff                     how to cite these materials
├── LICENSE                          CC BY 4.0, for the materials
└── LICENSE-CODE                     MIT, for the code
```

## Getting started

The hands-on sessions need Python with cobrapy, Escher, pandas, matplotlib and JupyterLab. Both set-ups below
have been tested: conda with Python 3.11, and pip with Python 3.12. cobrapy installs the free GLPK solver,
which is all this workshop needs. (For larger analyses, Gurobi or CPLEX are faster and free for academic use.)

1. **Get the material.** On this repository's GitHub page, click **Code → Download ZIP** and unzip it, or
   clone it with `git clone` and the URL shown under **Code**.

2. **Install the packages.** Open a terminal in the repository folder and use *one* of these options.

   **Option A: conda** (Anaconda, Miniconda or Miniforge)
   ```bash
   conda env create -f environment.yml
   conda activate code-m
   ```

   **Option B: pip in a virtual environment**
   ```bash
   python3 -m venv .venv              # Windows: py -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Check the installation.** This should print the cobrapy version without errors:
   ```bash
   python -c "import cobra, escher; print('cobrapy', cobra.__version__)"
   ```

4. **Start JupyterLab** from the repository folder, then open the notebooks from its file browser:
   ```bash
   jupyter lab
   ```

Next time, just activate the environment (`conda activate code-m`, or `source .venv/bin/activate`) and run
`jupyter lab`.

## Working through the notebooks

- **Keep the folder structure.** The notebooks find their model files and helper modules (`toy_helpers.py`,
  `kbase_models.py`, `day3_helpers.py`) by relative path, so open each notebook in its own folder and don't move
  files around.
- **Student versions.** The Day 2 and Day 3 notebooks are student versions. Replace each `...` in the ✍️ cells
  with your own code. ✅ checkpoint cells tell you whether you are on track, and 💬 marks a question to discuss
  with your neighbour. Cells after an unfinished ✍️ cell fail until it is completed. Versions with solutions are
  available from the instructors.
- **Day 1 demo.** In [Day1/2_1.ipynb](Day1/2_1.ipynb), put the path of the model to explore in
  `cobra.io.read_sbml_model('')`, for example `'iJO1366.xml'`.
- **Escher maps need an internet connection,** because the map viewer loads from the web. Escher's
  in-notebook widget is built for the classic Notebook interface, so in JupyterLab a map may not appear inside
  the notebook. In that case, save it with `builder.save_html("map.html")` and open the file in a web browser.
  The Day 1 and Day 3 notebooks save their maps as HTML files, and the Day 2 toy notebook also draws a static
  picture of the network.
- **Notebooks write files.** Besides Escher HTML maps (ignored by git), the Day 2 notebooks write
  `toybacter_fermentans.xml`, `toybacter_fermentans.json` and `my_scorecard.csv`. The repository includes a copy
  of each; your run replaces them, and `git checkout -- <file>` restores the original.
- **KBase (Day 2, hands-on B).** Building the drafts yourself needs a free [KBase](https://www.kbase.us) account.
  The notebook runs without one, on drafts the instructors built on 9 October 2026 (in
  [Day2/04_Models/](Day2/04_Models)). To use your own drafts, download them from KBase (*Export / Download data*)
  and change the file names in the notebook's `FILES` cell: `load_model()` reads the `.json` and `.json.zip`
  exports.

## Models and data

Some models appear in more than one day's folder, so that each day is self-contained.

| File | Organism | Source | Publication |
|---|---|---|---|
| `iJO1366.xml` (Day 1) | *Escherichia coli* K-12 MG1655 | [BiGG](https://bigg.ucsd.edu/models/iJO1366) | Orth et al., 2011, *Mol. Syst. Biol.* |
| `iMM904.xml` (Days 1 and 3) | *Saccharomyces cerevisiae* | [BiGG](https://bigg.ucsd.edu/models/iMM904) | Mo et al., 2009, *BMC Syst. Biol.* |
| `iML1515.xml` (Days 2 and 3) | *Escherichia coli* K-12 MG1655 | [BiGG](https://bigg.ucsd.edu/models/iML1515) | Monk et al., 2017, *Nat. Biotechnol.* |
| `iYO844.xml` (Day 2) | *Bacillus subtilis* 168 | [BiGG](https://bigg.ucsd.edu/models/iYO844) | Oh et al., 2007, *J. Biol. Chem.* |
| `iNF517.xml` (Day 2) | *Lactococcus lactis* subsp. *cremoris* MG1363 | [BiGG](https://bigg.ucsd.edu/models/iNF517) | Flahaut et al., 2013, *Appl. Microbiol. Biotechnol.* |
| `e_coli_core.xml` (Day 3) | *E. coli* core metabolism | [BiGG](https://bigg.ucsd.edu/models/e_coli_core) | Orth, Fleming and Palsson, 2010, *EcoSal Plus* |
| `e_coli_core.Core_metabolism.json` (Day 3) | Escher map of *E. coli* core | [Escher](https://escher.github.io) | King et al., 2015, *PLoS Comput. Biol.* |
| `*.RAST.mdl.json.zip` (Day 2) | the three Day 2 bacteria | Drafts built by the instructors with ModelSEED in KBase | see [the discussion materials README](Day2/05_Discussion_materials/README.md) |
| `toybacter_fermentans.*`, `toybacter_map.json` (Day 2) | *Toybacter fermentans* (fictional) | Made for this workshop | — |
| `memote_reports/*.html` (Day 2) | the six Day 2 models | MEMOTE 0.17.0 snapshot reports | Lieven et al., 2020, *Nat. Biotechnol.* |

## References and further reading

- **FBA, in three pages:** Orth JD, Thiele I, Palsson BØ (2010). What is flux balance analysis?
  *Nat. Biotechnol.* 28:245–248. [doi:10.1038/nbt.1614](https://doi.org/10.1038/nbt.1614)
- **cobrapy:** Ebrahim A, Lerman JA, Palsson BØ, Hyduke DR (2013). COBRApy: COnstraints-Based Reconstruction and
  Analysis for Python. *BMC Syst. Biol.* 7:74. [doi:10.1186/1752-0509-7-74](https://doi.org/10.1186/1752-0509-7-74).
  Documentation: [cobrapy.readthedocs.io](https://cobrapy.readthedocs.io)
- **Escher:** King ZA, Dräger A, Ebrahim A, et al. (2015). Escher: a web application for building, sharing, and
  embedding data-rich visualizations of biological pathways. *PLoS Comput. Biol.* 11:e1004321.
  [doi:10.1371/journal.pcbi.1004321](https://doi.org/10.1371/journal.pcbi.1004321)
- **BiGG Models:** King ZA, Lu J, Dräger A, et al. (2016). BiGG Models: a platform for integrating, standardizing
  and sharing genome-scale models. *Nucleic Acids Res.* 44:D515–D522.
  [doi:10.1093/nar/gkv1049](https://doi.org/10.1093/nar/gkv1049)
- **E. coli core model:** Orth JD, Fleming RMT, Palsson BØ (2010). Reconstruction and use of microbial metabolic
  networks: the core *Escherichia coli* metabolic model as an educational guide. *EcoSal Plus*.
  [doi:10.1128/ecosalplus.10.2.1](https://doi.org/10.1128/ecosalplus.10.2.1)
- **ModelSEED:** Henry CS, DeJongh M, Best AA, et al. (2010). High-throughput generation, optimization and analysis
  of genome-scale metabolic models. *Nat. Biotechnol.* 28:977–982.
  [doi:10.1038/nbt.1672](https://doi.org/10.1038/nbt.1672)
- **KBase:** Arkin AP, Cottingham RW, Henry CS, et al. (2018). KBase: the United States Department of Energy
  Systems Biology Knowledgebase. *Nat. Biotechnol.* 36:566–569. [doi:10.1038/nbt.4163](https://doi.org/10.1038/nbt.4163)
- **MEMOTE:** Lieven C, Beber ME, Olivier BG, et al. (2020). MEMOTE for standardized genome-scale metabolic model
  testing. *Nat. Biotechnol.* 38:272–276. [doi:10.1038/s41587-020-0446-y](https://doi.org/10.1038/s41587-020-0446-y)
- **More tools:** the [openCOBRA project](https://opencobra.github.io) collects COBRA software for Python, MATLAB
  and R.

## Citing these materials

If you use or adapt these materials, please cite them. GitHub's **Cite this repository** button (from
[CITATION.cff](CITATION.cff)) gives the reference in APA and BibTeX formats.

## License

- **Materials** (slides, notebook text and figures, run sheet and documentation): [CC BY 4.0](LICENSE). You may
  share and adapt them for any purpose, provided you give credit.
- **Code** (the helper modules `*.py` and the code in the notebooks): [MIT](LICENSE-CODE).
- **Third-party content** keeps its own terms: the models from BiGG Models, the Escher map, and any third-party
  figures reproduced in the slides. Please cite the original publications listed above.

## Authors

- Francesco Del Carratore
- Stephen Chapman

Questions, corrections and suggestions are welcome: please open an issue on this repository.

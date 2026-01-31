# A2199 Galaxy Cluster Luminosity Function Analysis

[![Python 3.12.5](https://img.shields.io/badge/python-3.12.5-blue.svg)](https://www.python.org/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)
[![License](https://img.shields.io/badge/license-TBD-lightgrey.svg)]()

**r-band luminosity function of the A2199 galaxy cluster, combining spectroscopy**

---

## Project Overview

This repository presents the analysis of the **A2199 galaxy cluster luminosity function (LF)**. It uses:

- **SDSS DR18 photometry** (~13,000 galaxies within 35 arcmin)
- **Spectroscopy** (~2,000 redshifts)
- **Cluster comparison:** A2199, Coma, Virgo
- **Field reference:** Blanton et al. (2005)
- **Simulation:** TNG50 (IllustrisTNG)

**Main Goals:**
1. Measure LF to faint magnitudes (M_r ≈ -13)
2. Fit Schechter function (φ*, M*, α)
3. Investigate faint-end slope upturn
4. Compare cluster vs field LFs
5. Find red sequence in clusters

## Repository Structure

```
Park2026a-A2199-LF/
├── CODE/
│   ├── DATA_ANALYSIS/
│   │   ├── 00_cluster_selection.ipynb
│   │   ├── 01_red_sequence_analysis.ipynb
│   │   ├── 02_spectroscopic_completeness.ipynb
│   │   └── 03_caustic_phase_space_diagram.ipynb
│   └── LF/
│       ├── 01_TNG50_luminosity_function.ipynb
│       ├── 02_A2199_luminosity_function.ipynb
│       ├── 03_Coma_luminosity_function.ipynb
│       ├── 04_Virgo_luminosity_function.ipynb
│       ├── 05_Field_luminosity_function.ipynb
│       └── 06_multi_cluster_LF_comparison.ipynb
├── DATA/
│   ├── A2199/
│   │   ├── Song2017/
│   │   ├── A2199_mastercat_within35arcmin.csv
│   │   └── ...
│   ├── Coma/
│   │   ├── coma_woody_master_catalog.npz
│   │   ├── 00_convert_to_csv.py
│   │   └── 01_kcorrect_galaxies.py
│   ├── Virgo/
│   │   ├── Ferrarese2020_tab4.txt
│   │   ├── Ferrarese2020_tab5.txt
│   │   ├── Ferrarese2020_tab6.txt
│   │   ├── Ferrarese2020_tab7.txt
│   │   ├── 00_read.py
│   │   └── 01_kcorrgal.py
│   ├── TNG50/
│   │   ├── TNG50_output_snapNum_96/
│   │   │   ├── Massive_Haloinfo_SnapNum96.csv
│   │   │   └── HALOCAT/
│   │   └── TNG50_output_snapNum_99/
│   │       ├── Massive_Haloinfo_SnapNum99.csv
│   │       └── HALOCAT/
│   ├── AllHeCS_VAC_updated.csv
│   ├── Blanton2005_Table2.csv
│   ├── Blanton2005correctionFactor.txt
│   ├── Ferrarese2020correctionFactor.csv
│   ├── A2199_Machine_Redable_Table3.txt
└── FIGURE/
    └── images/
        ├── A2199_LF.pdf
        ├── A2199_red_sequence.pdf
        ├── A2199_caustic.pdf
        ├── A2199_fspec.pdf
        ├── A2199_2Dfspec.pdf
        ├── A2199_fspec_vs_rpetro.pdf
        ├── A2199_spec_z_numbers.pdf
        ├── LF_normalized_comparison.pdf
        └── LF_param_comparison.pdf
```

## Key Analyses

### Data Analysis (`CODE/DATA_ANALYSIS/`)

- **00_cluster_selection.ipynb:** Cluster selection from HeCS (z < 0.04, N > 100), distance modulus, absolute magnitudes.
- **01_red_sequence_analysis.ipynb:** Color-magnitude diagram and red sequence fit (g-r vs r), compare literature and selection limits.
- **02_spectroscopic_completeness.ipynb:** f_spec vs magnitude and radius, completeness maps, comparison of Song+2017/SDSS/NED.
- **03_caustic_phase_space_diagram.ipynb:** Projected radius vs velocity, red/blue separation, caustic boundaries, phase space distributions.

### Luminosity Functions (`CODE/LF/`)

- Each notebook: data loading, extinction correction, binning in M_r, Schechter fitting with MCMC (emcee), uncertainty (16th/50th/84th), parameter/corner plots, comparisons.
- Multi-cluster and field comparison (Blanton+2005; TNG50 simulation).

## Requirements

```python
numpy
pandas
matplotlib
astropy
scipy
emcee
tqdm
corner
sklearn
```

## Included / Not Included Data

- `AllHeCS_VAC_updated.csv`: **NOT included** (contact HeCS-omnibus Team)
- `Blanton2005_Table2.csv`: included (field LF)
- Correction tables (Blanton/Ferrarese): included
- A2199 machine-readable LF: included

#### Large Files (NOT in GitHub):

- TNG50 simulation catalogs (`DATA/TNG50/TNG50_output_snapNum_96/HALOCAT/`, etc. >25,000 files, several GB)  
  Download from: [IllustrisTNG website](https://www.tng-project.org/)

## Citation

If you use this code or data, please read or cite:

```
A redshift survey of the nearby galaxy cluster Abell 2199 : No upturn of the faint-end slope of galaxy luminosity function
```
https://arxiv.org/abs/2601.21329v1

## Author

**Jong-In Park**  
Seoul National University  
jongin.park@snu.ac.kr  
2026


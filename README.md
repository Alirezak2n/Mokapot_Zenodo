
# Enhancing Peptide-Spectrum Match Identification

This repository contains the code and Jupyter notebook to recreate the manuscript's figures and rerun the entire pipeline.

## 📝 Paper Title

**Enhancing Peptide-Spectrum Match Identification: Leveraging Mokapot with Nonlinear Machine Learning Algorithms to Increase PSMs, with Consideration for False Positives**

📦 **[Zenodo Link](https://zenodo.org/record/1)**

## 👥 Authors

Alireza Nameni¹², Arthur Declercq¹², Ralf Gabriels¹², Sven Degroeve¹², Lennart Martens¹²,§, Robbin Bouwmeester¹²

**Affiliations**:  
¹ VIB-UGent Center for Medical Biotechnology, Ghent, Belgium  
² Department of Biomolecular Medicine, Ghent University, Ghent, Belgium

---

## 📂 Repository Structure
### You need to download the data from Zenodo and place it in the correct folders as described below, in order to run the pipeline and recreate the figures successfully.

- ML_Algorithms_results/
    - mokapot_svm/
    - random_forest/
    - xgboost/
- Peptideshaker_results/
    - PXD000561/
        - andromeda/
        - comet/
        - msgf/
        - msamanda/
        - msgf_noEntrapment/ (for some of the projects)
    - PXD000612/
    .
    .
    .
    - PXD040344/
- random_forest_csv_results/
- Scripts/
    - logging_setup.py
    - main.py (main script to run the pipeline)
    - mokapot_svm.py
    - rf_model.py
    - utilities.py
    - xg_model.py
- Figures.ipynb (Jupyter notebook to recreate the manuscript's figures)


## Data download
Due to size restriction, the data is not included in this repository. The data can be downloaded from Zenodo at the following link: [Zenodo Data](https://zenodo.org/record/1).

## Contact
For questions or support, please open an issue or contact alireza.nameni@ugent.be


This repository contain the code, and jupyter notebook to recreate the manuscript's figures and rerun the whole pipeline.

## Enhancing Peptide-Spectrum Match Identification: Leveraging Mokapot with Nonlinear Machine Learning Algorithms to Increase PSMs, with Consideration for False Positives_Zenodo

Authors: Alireza Nameni1,2, Arthur Declercq1,2, Ralf Gabriels1,2, Sven Degroeve 1,2, Lennart Martens1,2,§, Robbin Bouwmeester1,2

Affiliations:
1  VIB-UGent Center for Medical Biotechnology, Ghent, Belgium
2  Department of Biomolecular Medicine, Ghent University, Ghent,  Belgium

## Repository structure to recreate the manuscript's figures and rerun the whole pipeline
-ML_Algorithms_results
    -mokapot_svm
    -random_forest
    -xgboost
-Peptideshaker_results
    -PXD000561
        -andromeda
        -comet
        -msgf
        -msamanda
        -msgf_noEntrapment (for some pride projects)
    -PXD000612
    .
    .
    .
    -PXD040344
-random_forest_csv_results
-Scripts
    -logging_setup.py
    -main.py (main script to run the pipeline)
    -mokapot_svm.py
    -rf_model.py
    -utilities.py
    -xg_model.py
-Figures.ipynb (jupyter notebook to recreate the manuscript's figures)

## Data download
Due to size restriction, the data is not included in this repository. The data can be downloaded from Zenodo at the following link: [Zenodo Data](https://zenodo.org/record/1).

## Contact
For questions or support, please open an issue or contact alireza.nameni@ugent.be
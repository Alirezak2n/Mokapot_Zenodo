import mokapot
import time
import logging
import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from pathlib import Path
import logging_setup
import utilities
import numpy as np

# Set the random seed:
np.random.seed(1)

logging.getLogger("mokapot").setLevel(logging.WARNING)
logger = logging_setup.setup_logger('xgboost_logger',file_name='xg_logs.log')
temp_results_output_for_test = []

def mokapot_and_entrapment(model_name, ml_model, psms, save_folder_name):
    """
    Run Mokapot with the provided machine learning model and perform entrapment counting.
    Save the model and results to disk.
    """
    logger.info(f"--Starting Mokapot with {model_name}--")
    start_time = time.time()

    # Run Mokapot with the specified model
    results, mokapot_models = mokapot.brew(psms, model=ml_model, max_workers=32)

    elapsed_time = time.time() - start_time
    logger.info(f"--Mokapot finished in {elapsed_time:.2f} seconds with {model_name}--")

    # Define save paths
    folder_time = time.strftime("%Y%m%d")
    file_time = time.strftime("%H%M")
    save_path = Path(f'./saved_models/xgboost/{folder_time}_{save_folder_name}')
    save_path.mkdir(parents=True, exist_ok=True)

    # Save the model and results
    mokapot_models[0].save(f'{save_path}/{model_name}_{file_time}.pickle')
    results.to_txt(file_root=f'{save_path}/{model_name}_{file_time}')

    # Perform entrapment counting
    logger.info("--Starting entrapment counter--")
    start_time = time.time()
    entraps = utilities.main(psms_table=results.confidence_estimates['psms'], divider=';')
    elapsed_time = time.time() - start_time

    logger.info(
        f"--Entrapment counting finished in {elapsed_time:.2f} seconds, with {results.accepted['psms']} psms, "
        f"e_h {entraps[0]} and values of {entraps[1]} --"
    )

    # Store the results for this run
    temp_results_output_for_test.append({
        'model': model_name,
        'psms': results.accepted['psms'],
        'entraps': entraps
    })
    return True


def run_xgboost_model(pin_file, save_folder_name):
    """
    Run XGBoost with various hyperparameters on the given pin file.
    """
    logger.info(f"--Reading the pin file: {pin_file}--")
    start_time = time.time()
    psms = mokapot.read_pin(pin_file)
    logger.info(f"--The pin file was read in {time.time() - start_time:.2f} seconds--")

    # Define the parameter grid for GridSearchCV
    hyper_params = {
        'max_depth': [3, 5, 6],
        'learning_rate': [0.01, 0.1, 0.2],
        'n_estimators': [100, 200, 300],
        'subsample': [0.5, 0.7, 1.0],
        'colsample_bytree': [0.4, 0.6, 0.8]
    }

    # Initialize GridSearchCV with the XGBoost classifier
    gs = GridSearchCV(
        estimator=xgb.XGBClassifier(),
        param_grid=hyper_params,
        n_jobs=-1,
        verbose=5,
        cv=3
    )

    # Wrap GridSearchCV with Mokapot's model wrapper
    model_obj = mokapot.model.Model(gs)
    model_name = "XGBoost"

    # Run Mokapot and entrapment counting with the XGBoost model
    mokapot_and_entrapment(model_name, model_obj, psms, save_folder_name)

    # Log final results
    logger.info("Completed all XGBoost runs. Summary of results:")
    for result in temp_results_output_for_test:
        logger.info(f"Model {result['model']}: Accepted PSMS = {result['psms']}, Entraps = {result['entraps']}")

    return True




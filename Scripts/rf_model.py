import mokapot
import time
from sklearn.ensemble import RandomForestClassifier
import logging
from pathlib import Path
import logging_setup
import utilities
import numpy as np

# Set the random seed:
np.random.seed(1)

# Setup logging
logging.getLogger("mokapot").setLevel(logging.WARNING)
logger = logging_setup.setup_logger('rf_logger',file_name='rf_logs.log')

# Store results for all runs
temp_results_output_for_test = {}


def mokapot_and_entrapment(
        model_name,
        ml_model,
        psms,
        save_folder_name
):
    """
    Run Mokapot with the provided machine learning model and perform entrapment counting.
    Save the model and results to disk.
    """
    logger.info(f"--Starting Mokapot with random forest min_sample_leaf={ml_model.estimator.min_samples_leaf} , max_depth={ml_model.estimator.max_depth}--")
    start_time = time.time()

    # Run Mokapot with the specified model
    results, mokapot_models = mokapot.brew(psms, model=ml_model, max_workers=32)

    elapsed_time = time.time() - start_time
    logger.info(f"--Mokapot finished in {elapsed_time:.2f} seconds with {model_name}--")

    # Define save paths
    folder_time = time.strftime("%Y%m%d")
    file_time = time.strftime("%H%M")
    save_path = Path(f'./saved_models/random_forest/{folder_time}_{save_folder_name}')
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
    temp_results_output_for_test[(ml_model.estimator.min_samples_leaf, ml_model.estimator.max_depth)] = [results.accepted['psms']]

    return True


def run_random_forest(pin_file,save_folder_name):
    """
    Run Random Forest with various min_samples_leaf and max_depth values on the given pin file.
    """
    logger.info(f"--Reading the pin file: {pin_file}--")
    start_time = time.time()
    psms = mokapot.read_pin(pin_file)
    logger.info(f"--The pin file was read in {time.time() - start_time:.2f} seconds--")

    # Define the parameter grids
    min_samples_leaf_list = [4, 8, 16, 32, 64]
    max_depth_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 40]

    # Iterate over each combination of min_samples_leaf and max_depth
    for min_sample in min_samples_leaf_list:
        for max_depth in max_depth_list:

            # Initialize the Random Forest model with current parameters
            rf_base = RandomForestClassifier(
                n_estimators=200,
                max_depth=max_depth,
                min_samples_leaf=min_sample
            )
            model_rf = mokapot.model.Model(rf_base)
            model_name = f"rf_{min_sample}_{max_depth}"
            # Run Mokapot and entrapment counting with the Random Forest model
            mokapot_and_entrapment(model_name, model_rf, psms,save_folder_name)

    # Log final results
    logger.info("Completed all Random Forest runs. Summary of results:")
    for params, psms in temp_results_output_for_test.items():
        logger.info(f"Params {params}: Accepted PSMS = {psms[0]}")

    return True


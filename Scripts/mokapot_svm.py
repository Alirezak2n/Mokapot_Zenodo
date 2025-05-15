import mokapot
import time
import logging
from pathlib import Path
import numpy as np
import logging_setup
import utilities

# Set the random seed:
np.random.seed(1)

logging.getLogger("mokapot").setLevel(logging.WARNING)
logger = logging_setup.setup_logger('mokapot_svm_logger',file_name='MokapotSVM.log')


def percolator_model(train_subset=500000):
    perco = mokapot.PercolatorModel(subset_max_train=train_subset)
    return perco

def run_mokapot_svm(pin_file,save_folder_name):
    logger.info("--Reading the pin file--")
    start_time = time.time()
    psms = mokapot.read_pin(pin_file)
    logger.info(f"--The pin file is read in {time.time() - start_time :.2f} seconds--")

    logger.info("--Starting Mokapot with SVM--")
    model = percolator_model()
    results, mokapot_models = mokapot.brew(psms, model=model, max_workers=64)

    folder_time = time.strftime("%Y%m%d")
    file_time = time.strftime("%H%M")
    save_path = Path(f'./saved_models/mokapot_svm/{folder_time}_{save_folder_name}')
    save_path.mkdir(parents=True, exist_ok=True)

    mokapot_models[0].save(f'{save_path}/MokapotSVM_{file_time}.pickle')
    results.to_txt(file_root=f'{save_path}/MokapotSVM_{file_time}')

    logger.info(f"--Mokapot finished in {time.time() - start_time :.2f} seconds with Mokapot SVM--")

    logger.info("--Starting entrapment counter--")
    start_time = time.time()
    entraps = utilities.main(psms_table=results.confidence_estimates['psms'], divider=';')
    logger.info(f"--Entrapment counting finished in  {time.time() - start_time :.2f} seconds--")
    logger.info(f"--Mokapot SVM has {results.accepted['psms']} psms, e_h {entraps[0]} and values of {entraps[1]}--")

    return True



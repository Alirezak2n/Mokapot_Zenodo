import os
from mokapot_svm import run_mokapot_svm
from rf_model import run_random_forest
from xg_model import run_xgboost_model

def main(directory='E:/Peptideshaker_results/'):

    for pxd_folder in os.listdir(directory):
        pxd_path = os.path.join(directory, pxd_folder)
        for engine_type in ["andromeda", "comet", "msamanda", "msgf"]:
            engine_path = os.path.join(pxd_path, engine_type)
            # Check if the engine folder exists
            if os.path.exists(engine_path):
                for file_name in os.listdir(engine_path):
                    if file_name.endswith(".pin"):
                        pin_file = os.path.join(engine_path, file_name)
                        print(f"Processing {pin_file}...")
                        save_folder_name = f"{pxd_folder}_{engine_type}"
                        # Run Mokapot SVM
                        run_mokapot_svm(pin_file,save_folder_name)
                        # Run Random Forest
                        run_random_forest(pin_file,save_folder_name)
                        # Run XGBoost
                        run_xgboost_model(pin_file,save_folder_name)
    return True


if __name__ == '__main__':
    main()

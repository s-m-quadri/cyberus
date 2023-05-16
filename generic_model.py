import shutil
import pickle
import py7zr
import sys
import os

DATASET_DIR = os.path.abspath("datasets")
CYBERUS_MODEL_DIR = "cyberus_model"


class cyberus_model:
    # Storing model and features
    store = {}


class cyberus_core:
    def __init__(self) -> None:
        self.load_cyberus_model(CYBERUS_MODEL_DIR)

    def unpack(self):
        if os.path.exists(path=DATASET_DIR):
            return

        if os.path.isfile("datasets.7z"):
            with py7zr.SevenZipFile("datasets.7z", "r") as archive:
                archive.extractall()

        else:
            print("Dataset do not exist, download from:")
            print(
                "https://drive.google.com/drive/folders/1xOIc_d3RDOKhaoowChTubQ101nWpZq7Q")
            print("... have you done? make sure 'datasets.7z' is in runtime directory.")
            print("... type 'yes' to continue >> ", end="")
            if input() != "yes":
                sys.exit()
            self.unpack()

    def load_cyberus_model(self, filename):
        self.cyberus_model = cyberus_model()
        if os.path.exists(filename):
            self.cyberus_model.store = pickle.load(
                open(CYBERUS_MODEL_DIR, "rb"))

    def save_cyberus_model(self):
        pickle.dump(self.cyberus_model.store, open(CYBERUS_MODEL_DIR, "wb"),
                    protocol=pickle.HIGHEST_PROTOCOL)
        
        
    def __del__(self):
        if os.path.exists(path=DATASET_DIR):
            shutil.rmtree(DATASET_DIR)

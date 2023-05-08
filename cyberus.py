import pandas
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn import metrics
import os
import shutil
import pickle
import py7zr
import sys

DATASET_DIR = os.path.abspath("datasets")
CYBERUS_MODEL_DIR = "cyberus_model"
PATH_SPAM_SMS_DATASET = os.path.join(DATASET_DIR, "spam_sms.csv")
PATH_SPAM_MAILS_DATASET = os.path.join(DATASET_DIR, "spam_mails.csv")


class CyberusModel:
    # Storing model and features
    store = {}


class Cyberus:
    def __init__(self) -> None:
        self.unpack()
        self.load_cyberus_model(CYBERUS_MODEL_DIR)
        self.load_spam_sms(PATH_SPAM_SMS_DATASET)
        self.load_spam_mails(PATH_SPAM_MAILS_DATASET)

    def save_cyberus_model(self):
        pickle.dump(self.cyberus_model.store, open(CYBERUS_MODEL_DIR, "wb"),
                    protocol=pickle.HIGHEST_PROTOCOL)

    def unpack(self):
        if os.path.exists(path=DATASET_DIR):
            print("exits")
            return

        if os.path.isfile("datasets.7z"):
            with py7zr.SevenZipFile("datasets.7z", "r") as archive:
                archive.extractall()

        else:
            print("Dataset do not exist, download from:")
            print(
                "https://drive.google.com/drive/folders/1xOIc_d3RDOKhaoowChTubQ101nWpZq7Q?usp=share_link")
            print("... have you done")
            print("... type 'yes' to continue >> ", end="")
            if input() != "yes":
                sys.exit()
            self.unpack()

    def __del__(self):
        if os.path.exists(path=DATASET_DIR):
            shutil.rmtree(DATASET_DIR)

    def load_cyberus_model(self, filename):
        self.cyberus_model = CyberusModel()
        if os.path.exists(filename):
            self.cyberus_model.store = pickle.load(
                open(CYBERUS_MODEL_DIR, "rb"))

    def load_spam_sms(self, filename):
        # Load dataset
        self.dataset = pandas.read_csv(filename)

        # Update feature: Convert labels to numeric data
        self.dataset.rename(columns={
            "v1": "label",
            "v2": "body"
        }, inplace=True)

        # Call generic method to load
        self.load_spam_model("sms")

    def load_spam_mails(self, filename):
        # Load dataset
        self.dataset = pandas.read_csv(filename)

        # Update feature: Convert labels to numeric data
        self.dataset.rename(columns={
            "text": "body"
        }, inplace=True)

        # Call generic method to load
        self.load_spam_model("mails")

    def load_spam_model(self, title: str):
        if self.cyberus_model.store.get(title, None):
            return

        # Split Feature as input and labelled output
        X = self.dataset["body"]
        y = self.dataset["label"].map({"spam": 1, "ham": 0})

        # Split data as training and testing
        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # Tokenize in column format
        # i.e. extracting features from "body"
        vectorize = CountVectorizer(
            stop_words='english', strip_accents="ascii", lowercase=True)
        vectorize.fit(X)
        features = vectorize.get_feature_names_out()

        # Transform splitted data, as accordance with tokens
        # as matrix of Document Frequency
        X_train_dtm = vectorize.transform(X_train)
        X_test_dtm = vectorize.transform(X_test)

        # Weight Frequency, i.e. reduce weight of more frequent
        # token across documents as matrix of Inverse Document Frequency
        transformer = TfidfTransformer()
        transformer.fit(X_train_dtm)
        X_train = transformer.transform(X_train_dtm).toarray()
        X_test = transformer.transform(X_test_dtm).toarray()

        # Build Model
        modal = LinearSVC()
        modal.fit(X_train, y_train)

        # Measure the goodness of model
        y_predict = modal.predict(X_test)
        score = metrics.accuracy_score(y_true=y_test, y_pred=y_predict)
        print(
            f"Spam {title.title()} Model created with {score*100:.2f}% accuracy.")

        # Save the model, to avoid re_calculations
        self.cyberus_model.store[title] = {
            "modal": modal,
            "features": features,
        }
        self.save_cyberus_model()

    def judge_spam_sms(self, text):
        return self.judge(text, "sms")

    def judge_spam_mails(self, text):
        return self.judge(text, "mails")

    def judge(self, text: str, title: str):
        # Tokenize the input
        vectorize = CountVectorizer(
            stop_words='english', strip_accents="ascii", lowercase=True)
        vectorize.fit(self.cyberus_model.store[title]["features"])
        input_text_dtf = vectorize.transform([text])

        # Weight the input
        transformer = TfidfTransformer()
        transformer.fit(input_text_dtf)
        input_text = transformer.transform(input_text_dtf).toarray()

        # Predict the output
        result = self.cyberus_model.store[title]["modal"].predict(input_text)
        return True if result == 1 else False

    def get_cyberus_score(self, text):
        return [
            self.judge_spam_sms(text),
            self.judge_spam_mails(text),
        ]


if __name__ == "__main__":
    obj = Cyberus()
    results = obj.get_cyberus_score("Free offer free")
    print(results)

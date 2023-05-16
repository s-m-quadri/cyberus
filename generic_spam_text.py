from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn import metrics
import os
import pandas

from generic_model import *


class generic_spam_text:

    def __init__(self, database_names: list()) -> None:
        self.memory = cyberus_core()
        self.database_names = database_names
        self.load_text_datasets()

    def load_text_datasets(self):
        """
        On given object, load all the dataset, whose list is provided 
        during the initialization of this class
        """
        for model_name in self.database_names:
            # If given model already exist in the ram,
            # just ignore whole process
            if self.memory.cyberus_model.store.get(model_name, None):
                continue
            
            # Unpack the datasets
            self.memory.unpack()
            
            # Load from CSV file
            self.dataset = pandas.read_csv(
                os.path.join(DATASET_DIR, model_name + ".csv"))
            
            # Cleanup - using the function provided by calling class
            # and load dataset
            self.database_names[model_name](self)
            self.load_spam_model(model_name)

    def load_spam_model(self, model_name: str):
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
            f"+ {model_name.title()} Model created with {score*100:.2f}% accuracy.")

        # Save the model, to avoid re_calculations
        self.memory.cyberus_model.store[model_name] = {
            "modal": modal,
            "features": features,
        }
        self.memory.save_cyberus_model()

    def judge(self, text: str, dataset_name: str):
        # Tokenize the input
        vectorize = CountVectorizer(
            stop_words='english', strip_accents="ascii", lowercase=True)
        vectorize.fit(self.memory.cyberus_model.store[dataset_name]["features"])
        input_text_dtf = vectorize.transform([text])

        # Weight the input
        transformer = TfidfTransformer()
        transformer.fit(input_text_dtf)
        input_text = transformer.transform(input_text_dtf).toarray()

        # Predict the output
        result = self.memory.cyberus_model.store[dataset_name]["modal"].predict(
            input_text)
        return True if result == 1 else False

    def judge_all(self, text):
        return [self.judge(text, x) for x in self.database_names]
    
    def get_memory(self):
        return self.memory.cyberus_model.store


class spam_text(generic_spam_text):

    def dataset_spam_sms(self):
        self.dataset.rename(columns={
            "v1": "label",
            "v2": "body"
        }, inplace=True)

    def dataset_spam_mails(self):
        self.dataset.rename(columns={
            "text": "body"
        }, inplace=True)

    TEXT_DATASET_NAMES = {
        "spam_sms": dataset_spam_sms,
        "spam_mails": dataset_spam_mails,
    }

    def __init__(self) -> None:
        super().__init__(self.TEXT_DATASET_NAMES)

    def judge_all(self, text):
        return super().judge_all(text)

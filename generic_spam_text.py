from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn import metrics
import os
import pandas

DATASET_DIR = os.path.abspath("datasets")


class generic_spam_text:

    def __init__(self, database_names: list()) -> None:
        self.database_names = database_names
        self.load_text_datasets()

    def load_text_datasets(self):
        for dataset in self.database_names:
            self.dataset = pandas.read_csv(
                os.path.join(DATASET_DIR, dataset + ".csv"))
            self.database_names[dataset](self)
            self.load_spam_model(dataset)

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
            f"+ {title.title()} Model created with {score*100:.2f}% accuracy.")

        # Save the model, to avoid re_calculations
        self.cyberus_model.store[title] = {
            "modal": modal,
            "features": features,
        }
        self.save_cyberus_model()

    def judge(self, text: str, dataset_name: str):
        # Tokenize the input
        vectorize = CountVectorizer(
            stop_words='english', strip_accents="ascii", lowercase=True)
        vectorize.fit(self.cyberus_model.store[dataset_name]["features"])
        input_text_dtf = vectorize.transform([text])

        # Weight the input
        transformer = TfidfTransformer()
        transformer.fit(input_text_dtf)
        input_text = transformer.transform(input_text_dtf).toarray()

        # Predict the output
        result = self.cyberus_model.store[dataset_name]["modal"].predict(
            input_text)
        return True if result == 1 else False

    def judge_all(self, text):
        return [self.judge(text, x) for x in self.database_names]

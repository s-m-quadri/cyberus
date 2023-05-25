from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
import os
import pandas

import seaborn
import matplotlib.pyplot as plt
import numpy


from generic_model import *


class generic_spam_url:

    def __init__(self, database_names: list()) -> None:
        self.memory = cyberus_core()
        self.database_names = database_names
        self.load_url_datasets()

    def load_url_datasets(self):
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
            self.build_model(model_name)

    def pre_process_spam_model(self):
        # Function:
        # Cumulative counts of 'token' for 'scan_dir' directives,
        # i.e. list obtained by splitting url w.r.t '/'
        def add_count(token: str, scan_dir: int = 0):
            match scan_dir:
                case 0:
                    def count_function(url): return url.count(token)
                    new_col = self.dataset["url"].apply(count_function)
                    new_col = new_col.to_frame(name=f"count({token})")
                    self.dataset = pandas.concat(
                        [self.dataset, new_col], axis=1)
                case _:
                    def count_function(url: str):
                        counts = 0
                        dirs = [x for x in url.split("/") if x != ""]
                        for dir in dirs[:scan_dir]:
                            counts = counts + dir.count(token)
                        return counts
                    new_col = self.dataset["url"].apply(count_function)
                    new_col = new_col.to_frame(
                        name=f"count({token})/({scan_dir})")
                    self.dataset = pandas.concat(
                        [self.dataset, new_col], axis=1)

        def add_count_rigorously(token: str):
            for i in range(6):
                add_count(token, i)

        # Function:
        # Counts of length for 'scan_dir' directives,
        # (cumulatively or non-cumulatively)
        def add_length(scan_dir: int = 0, cumulative: bool = True):
            match scan_dir:
                case 0:
                    def len_function(url): return len(url)
                    new_col = self.dataset["url"].apply(len_function)
                    new_col = new_col.to_frame(name=f"len")
                    self.dataset = pandas.concat(
                        [self.dataset, new_col], axis=1)
                case _:
                    def len_function(url: str):
                        try:
                            dirs = [x for x in url.split("/") if x != ""]
                            if cumulative:
                                return sum([len(x) for x in dirs[:scan_dir]])
                            return len(dirs[scan_dir])
                        except:
                            return 0
                    new_col = self.dataset["url"].apply(len_function,)
                    new_col_name = f"{'cml_' if cumulative else ''}len/({scan_dir})"
                    new_col = new_col.to_frame(name=new_col_name)
                    self.dataset = pandas.concat(
                        [self.dataset, new_col], axis=1)

        # Features: prefixes for urls
        prefixes_features = ["www.", "http:", "https:", "ftp:"]
        for feature in prefixes_features:
            add_count_rigorously(feature)

        # Features: top-level domains
        tlds = ["COM", "NET", "ORG", "JP", "DE", "UK", "FR", "BR", "IT", "RU", "ES", "ME", "GOV", "PL", "CA", "AU", "CN", "CO", "IN", "NL",
                "EDU", "INFO", "EU", "CH", "ID", "AT", "KR", "CZ", "MX", "BE", "TV", "SE", "TR", "TW", "AL", "UA", "IR", "VN", "CL", "SK", "LY",
                "CC", "TO", "NO", "FI", "US", "PT", "DK", "AR", "HU", "TK", "GR", "IL", "NEWS", "RO", "MY", "BIZ", "IE", "ZA", "NZ", "SG", "EE",
                "TH", "IO", "XYZ", "PE", "BG", "HK", "RS", "LT", "LINK", "PH", "CLUB", "SI", "SITE", "MOBI", "BY", "CAT", "WIKI", "LA", "GA", "CF", "HR",
                "NG", "JOBS", "ONLINE", "KZ", "UG", "GQ", "AE", "IS", "LV", "PRO", "FM", "TIPS", "MS", "SA", "APP", "LAT", "PK", "WS", "TOP", "PW", "AI",
                ]
        for tld in tlds:
            add_count(f".{tld.lower()}")

        # Features: special symbols
        other_features = ["/", "?", "=", "&", ":"]
        for feature in other_features:
            add_count(feature)

        # Features: length of directives, cumulative and non-cumulatively
        for i in range(1, 6):
            add_length(i, cumulative=True)
        for i in range(11):
            add_length(i, cumulative=False)

    def build_model(self, model_name: str):
        # Pre processing
        self.pre_process_spam_model()

        # Split Feature as input and labelled output
        y = self.dataset["label"].map({"bad": 1, "good": 0})
        X = self.dataset.drop(columns=["label", "url"])

        # Split data as training and testing
        X_train, X_test, y_train, y_test = train_test_split(X, y)

        # Build Model
        modal = DecisionTreeClassifier(max_depth=15)
        modal.fit(X_train, y_train)

        # Measure the goodness of model
        y_predict = modal.predict(X_test)
        score = metrics.accuracy_score(y_true=y_test, y_pred=y_predict)
        print(
            f"+ {model_name.title()} Model created with {score*100:.2f}% accuracy.")
        print(metrics.confusion_matrix(y_test, y_predict))
        # Graphical Representation
        """
        cf_matrix = metrics.confusion_matrix(y_test, y_predict)
        plot_ = seaborn.heatmap(
            cf_matrix/numpy.sum(cf_matrix), annot=True, fmt='0.2%')
        plt.show()
        plot_ = seaborn.countplot(data=self.dataset, x="label")
        plt.show()
        """

        # Save the model, to avoid re_calculations
        self.memory.cyberus_model.store[model_name] = {
            "modal": modal,
            "features": X.columns.to_list(),
        }
        self.memory.save_cyberus_model()

    def judge(self, url: str, dataset_name: str):
        self.dataset = pandas.DataFrame.from_dict({"url": [url]})
        self.pre_process_spam_model()
        X = self.dataset.drop(columns=["url"])
        result = self.memory.cyberus_model.store[dataset_name]["modal"].predict(
            X)
        return True if result == 1 else False

    def judge_all(self, url):
        return [self.judge(url, x) for x in self.database_names]


class spam_url(generic_spam_url):

    def dataset_malicious_urls(self):
        def simplify_type(text):
            return "good" if text == "benign" else "bad"

        self.dataset["label"] = self.dataset["type"].apply(simplify_type)
        self.dataset.drop(columns=["type"], inplace=True)

    URL_DATASET_NAMES = {
        "malicious_urls": dataset_malicious_urls,
    }

    def __init__(self) -> None:
        super().__init__(self.URL_DATASET_NAMES)

    def judge_all(self, url):
        return super().judge_all(url)

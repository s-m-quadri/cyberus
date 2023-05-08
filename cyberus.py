
from generic_model import *
from generic_spam_text import *


class cyberus (generic_cyberus, generic_spam_text):

    def dataset_spam_sms(self):
        self.dataset.rename(columns={
            "v1": "label",
            "v2": "body"
        }, inplace=True)

    def dataset_spam_mails(self):
        self.dataset.rename(columns={
            "text": "body"
        }, inplace=True)

    DATASET_NAMES = {
        "spam_sms": dataset_spam_sms,
        "spam_mails": dataset_spam_mails,
    }

    def get_cyberus_score(self, text):
        return self.judge_all(text)

    def __init__(self) -> None:
        generic_cyberus.__init__(self)
        generic_spam_text.__init__(self, self.DATASET_NAMES)


if __name__ == "__main__":
    obj = cyberus()
    input_text = input("> Enter the text: ")
    results = obj.get_cyberus_score(input_text)
    print(f"> Risk found {results.count(True)} out of {len(results)},")
    print(f" ... or {results.count(True)/len(results)*100}%")

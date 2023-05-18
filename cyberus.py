
from generic_model import *
from generic_spam_text import *
from generic_spam_url import *
from banners import *


import re
import os


def main():
    cyberus_obj = cyberus()
    while True:
        if not cyberus_obj.get_input(singleline=False):
            break
        cyberus_obj.process()
        cyberus_obj.print()
        input("Press any key to continue...")


class cyberus:
    def __init__(self) -> None:
        self.spam_text_instance = spam_text()
        self.spam_url_instance = spam_url()
        self._cleanup_()

    def _cleanup_(self):
        self.input_text = ""
        # No result can be 0% risky, some risk always involved.
        # and not result can be 100%, some possibility of safety
        # is always exist, thus add padding to those values.
        self.results = [True, False]
        # Clean output screen
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def get_input(self, singleline=False):
        if singleline:
            return self._singleline_prompt_()
        return self._multiline_prompt_()

    def _singleline_prompt_(self):
        print(PROMPT_BANNER_SINGLE_LINE)
        self.input_text = input(">> ")

        # More check on first line
        if self.input_text.lower().strip() == "exit":
            return False

        # Indicating that got some useful
        return True

    def _multiline_prompt_(self):
        # Starting with fresh
        self._cleanup_()

        # Prompt banner
        print(INTRO_BANNER)
        print(PROMPT_BANNER)
        self.input_text = input()

        # More check on first line
        if self.input_text.lower().strip() == "exit":
            return False

        # Take multiple lines
        while True:
            try:
                line = input()
            except EOFError:
                return True
            self.input_text += f"\n{line}"

    def _judge_text_(self):
        res = self.spam_text_instance.judge_all(self.input_text)
        self.results.extend(res)

    def _judge_url_(self):
        res = []
        urls = re.findall(r"(?:https|http|ftp)\S*", self.input_text)
        for url in urls:
            for ins_res in self.spam_url_instance.judge_all(url):
                res.append(ins_res)
        self.results.extend(res)

    def process(self):
        self._judge_text_()
        self._judge_url_()

    def get_results(self):
        return self.results

    def get_score(self):
        score = self.results.count(True)/len(self.results)*100
        return round(score, 2)

    def print(self):
        score = self.get_score()
        if score >= 50:
            print(INDICATOR_HIGH)
        elif score > 20:
            print(INDICATOR_MEDIUM)
        else:
            print(INDICATOR_LOW)
        result_string = f"{score:.2f}% ({self.results.count(True)} out of {len(self.results)})."
        print("  >  Cyberus Risc Score: " + result_string)
        print(INDICATOR_END)


if __name__ == "__main__":
    main()

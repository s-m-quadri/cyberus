
from generic_model import *
from generic_spam_text import *
from generic_spam_url import *
from banners import *


import re
import os


def main():
    cyberus_prompt()
    return


def cyberus_prompt():

    while True:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
        print(INTRO_BANNER)
        print(PROMPT_BANNER)
        input_text = input(">> ")

        if input_text.lower().strip() == "exit":
            break

        while True:
            try:
                line = input()
            except EOFError:
                break
            else:
                input_text += f"\n{line}"

        results = get_results(input_text)
        score = get_cyberus_score(results)
        if score >= 50:
            print(INDICATOR_HIGH)
        elif score > 20:
            print(INDICATOR_MEDIUM)
        else:
            print(INDICATOR_LOW)
        result_string = f"{score:.2f}% ({results.count(True)} out of {len(results)})."
        print("  >  Cyberus Risc Score: " + result_string)
        print(INDICATOR_END)

        input("Press any key to continue...")


def get_cyberus_score(results):
    score = results.count(True)/len(results)*100
    return round(score, 2)


def get_results(input_text: str):
    urls = get_urls(input_text)
    results = cyberus_judge_text(input_text)
    results.extend(cyberus_judge_url(urls))
    return results


def get_urls(input_text: str):
    return re.findall(r"(?:https|http|ftp)\S*", input_text)


def cyberus_judge_text(all_text: str, instance=spam_text()):
    return instance.judge_all(text=all_text)


def cyberus_judge_url(urls: list, instance=spam_url()):
    result = []
    for url in urls:
        for ins_res in instance.judge_all(url):
            result.append(ins_res)
    return result


if __name__ == "__main__":
    main()

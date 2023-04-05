from typing import Union
from json import loads
from modules.api import get_data
from modules.own_types import Answers, Vocabulary

DELIM_HEADER = "# "
DELIM_ANSWERS = " / "


def get_extension(filename: str) -> str:
    return filename.split(".")[1]


def get_task(raw: str) -> str:
    task = raw.strip()
    if DELIM_HEADER in task:
        task = task.split(DELIM_HEADER)[1]
    return task


def get_answers(raw: str) -> Answers:
    raw = raw.strip()

    answers: Answers = [raw] \
        if DELIM_ANSWERS not in raw \
        else raw.split(DELIM_ANSWERS)

    return answers


def get_words(filename: Union[str,  None]) -> Vocabulary:
    words: Vocabulary = dict()

    if filename is None:
        return get_data()

    extension = get_extension(filename)

    with open(filename, "r") as f:
        if extension in set(["md", "txt"]):
            for line in f:
                line = line.strip()
                if line == "":
                    continue

                if "=" not in line:
                    continue

                task, answers_raw = line.split("=")

                task = get_task(task)
                words[task] = get_answers(answers_raw)

        if extension in set(["json"]):
            words = loads(f.read())

    return words

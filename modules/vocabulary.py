from random import randrange
from typing import List, Tuple
from modules.progress import reset_progress
from modules.own_types import Vocabulary, Answers, Counter


DELIM_ANSWERS = " / "
SPECIAL_CHARS = {"ñ": "ň", "ü": "\"u"}
HELP_RESPONSES = {"h", "help"}
END_RESPONSES = {"q", "quit"}
RESET_RESPONSES = {"r", "reset"}


def get_record(words: Vocabulary) -> Tuple[str, Answers]:
    all_keys: List[str] = list(words.keys())
    idx = randrange(len(all_keys))
    task = all_keys[idx]
    return task, words[task]


def skip_word(guessed: bool, count: int) -> bool:
    if guessed and count != 0:
        rand_n = randrange(0, 100) / 100
        if rand_n <= 1 / count:
            return True

    return False


def replace_special_chars(word: str) -> str:
    for special_char in SPECIAL_CHARS:
        word = word.replace(special_char, SPECIAL_CHARS[special_char])
    return word


def format_words(words: Answers) -> Answers:
    result = words.copy()
    for word in result:
        result.remove(word)
        result.append(replace_special_chars(word).lower())
    return result


def get_count_guessed(used_words: Counter) -> int:
    return [used_words[word][0]
            for word in used_words.keys()].count(True)


def help() -> None:
    print("response:")
    print("\th, help\t\tprints this help")
    print("\tq, quit\t\tends the session")
    print("\tr, reset\tresets the progress")
    print()


def play(words: Vocabulary, used_words: Counter) -> None:
    count_tasks = len(words)
    count_guessed = get_count_guessed(used_words)

    while True:
        if count_guessed == count_tasks:
            print("You guessed all the words. ADIOS")
            return

        task, corr_answers = get_record(words)

        guessed, count_used = used_words.get(task, (False, 0))
        if skip_word(guessed, count_used):
            continue

        print(task, "=", end=" ")
        response = input().strip()

        if response in HELP_RESPONSES:
            help()
            continue

        if response in END_RESPONSES:
            return None

        if response in RESET_RESPONSES:
            reset_progress()
            continue

        formatted = format_words(corr_answers)
        if response in formatted:
            if not guessed:
                used_words[task] = (True, count_used + 1)
                count_guessed += 1
            else:
                used_words[task] = (guessed, count_used - 1)

            print(f"Correct ({count_guessed} / {count_tasks})\n")
            continue

        print(f"Wrong -> {DELIM_ANSWERS.join(corr_answers)}\n")
        used_words[task] = (guessed, count_used + 1)

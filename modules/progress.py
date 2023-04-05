from modules.own_types import Counter
from json import dumps, loads
from modules.constants import PROGRESS_FILE


def save_progress(words: Counter) -> None:
    with open(PROGRESS_FILE, "w") as f:
        print(dumps(words), file=f)


def reset_progress() -> None:
    save_progress(dict())
    print("Progress reset\n")


def load_progress() -> Counter:
    try:
        with open(PROGRESS_FILE, "r") as f:
            words: Counter = loads(f.read())
            return words
    except OSError:
        reset_progress()
        return load_progress()

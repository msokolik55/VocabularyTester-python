from modules.vocabulary import help, play
# from modules.api import alter_offline
from modules.filler import get_words
from modules.progress import load_progress, save_progress
from modules.own_types import Vocabulary, Counter

FILE_NAME = "data/vocabulary.md"


def main() -> None:
    words: Vocabulary = get_words(FILE_NAME)
    # try:
    #    if alter_offline():
    #        print("New version of words downloaded to offline file.")
    # except ConnectionError:
    #    pass

    used_words: Counter = load_progress()
    try:
        help()
        play(words, used_words)
    except Exception as e:
        print(e)
    finally:
        save_progress(used_words)

    return None


main()

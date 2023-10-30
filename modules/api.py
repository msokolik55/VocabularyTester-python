from requests import get
from json import loads, dumps
# from dotenv import dotenv_values
from typing import Dict
from modules.own_types import Vocabulary
from modules.constants import OFFLINE_DATAFILE

# config = dotenv_values(".env")


def parse_env(key: str) -> str:
    # value = config.get(key, "")
    # return "" if value is None else value
    return ""


URL = parse_env("API_URL")
HEADERS = {
    'X-Access-Key':
        parse_env("API_ACCESS_PASSWORD")
}


def get_data() -> Vocabulary:
    req = get(URL, json=None, headers=HEADERS)
    data: Dict[str, Vocabulary] = loads(req.text)
    return data["record"]


def alter_offline() -> bool:
    api_words = get_data()

    with open(OFFLINE_DATAFILE, "r") as f:
        file_words = loads(f.read())
        if file_words == api_words:
            return False

    with open(OFFLINE_DATAFILE, "w") as f:
        print(dumps(api_words, indent=2), file=f)

    return True

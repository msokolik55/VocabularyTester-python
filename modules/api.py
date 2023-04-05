from requests import get
from json import loads, dumps
from typing import Dict
from modules.own_types import Vocabulary
from modules.constants import OFFLINE_DATAFILE

URL = 'https://api.jsonbin.io/v3/b/641cb7aeebd26539d095fee7/latest'
HEADERS = {
    'X-Master-Key':
        '$2b$10$EuWtqsDbYl7LBtzmH86A3OhYPtMPzVlf88YCTEvFsNyMg9crOcTKS'
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

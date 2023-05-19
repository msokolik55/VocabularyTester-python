from language import Language
from threading import Thread

SHORTS = ["en", "de"]

threads = [Thread(target=Language, args=[short]) for short in SHORTS]
for t in threads:
    t.start()

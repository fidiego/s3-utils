#!/bin/python3
from datetime import datetime
from hashlib import sha256

import logging
import os
import random
import sys

from jinja2 import Template
import boto3
import json


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_random_word(path):
    with open(path, "r") as openfile:
        words = openfile.readlines()
        return words[random.randrange(0, len(words)) + 1].strip()


def random_bucket_name():
    adjective = get_random_word(os.path.join(BASE_DIR, "words", "adjectives.txt"))
    noun = get_random_word(os.path.join(BASE_DIR, "words", "nouns.txt"))
    now = datetime.utcnow().isoformat()
    return f"{adjective}-{noun}-{sha256(now.encode()).hexdigest()[-8:]}"


if __name__ == "__main__":
    logger.warning("preparing to generate a random name")
    name = random_bucket_name()
    sys.stdout.write(name)
    logger.warning(f' - generated random name: {name}')

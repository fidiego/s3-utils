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


def get_args(args):
    if len(args) == 1:
        name = random_bucket_name()
    else:
        name = args[1]

    username = f"{name}-user"
    bucketname = name
    policy_name = (
        f'{"".join([n.lower().capitalize() for n in name.split("-")])}AccessPolicy'
    )
    return username, bucketname, policy_name


def gen_template(bucketname):
    with open(os.path.join(BASE_DIR, "policy.json.jinja2")) as openfile:
        template = Template(openfile.read())
        policy_name = template.render(bucketname=bucketname)
        return policy_name


if __name__ == "__main__":
    username, bucketname, policy_name = get_args(sys.argv)

    logger.warning(f"Preparing to create bucket, policy, and user")

    # initialize aws clients
    IAM, S3 = boto3.client("iam"), boto3.client("s3")

    # 1. create bucket
    S3.create_bucket(ACL="private", Bucket=bucketname)
    logger.warning(f" - created bucket: {bucketname}")

    # 2. create policy
    policy_document = gen_template(bucketname)
    policy_req = IAM.create_policy(
        PolicyName=policy_name,
        PolicyDocument=policy_document,
        Description=f"{policy_name} - genrated by s3utils script.",
    )
    policy_arn = policy_req["Policy"]["Arn"]
    logger.warning(f" - created policy: {policy_arn}")

    # 3. create user
    user_req = IAM.create_user(UserName=username)
    user = boto3.resource("iam").User(username)
    access_key_pair = user.create_access_key_pair()

    # 4. attach policy to user
    attach_req = IAM.attach_user_policy(UserName=username, PolicyArn=f"{policy_arn}")

    # 5. generate a file for the credentials
    with open(os.path.join(BASE_DIR, "buckets", f"{bucketname}.txt"), "w+") as openfile:
        with open(os.path.join(BASE_DIR, "bucket.txt.jinja2")) as opentemplate:
            template = Template(opentemplate.read())
            credentials = template.render(
                bucketname=bucketname,
                username=username,
                access_key_id=access_key_pair.id,
                access_key_secret=access_key_pair.secret,
                policy_arn=policy_arn,
            )
            openfile.write(credentials)
            logger.warning(f" - wrote credentials to {bucketname}.txt")

    # 6. log some ish
    logger.warning(f"Created bucket, policy, and user")
    logger.warning(f" -   user name: {username}")
    logger.warning(f" - bucket name: {bucketname}")
    logger.warning(f" - policy name: {policy_name}\n")
    logger.warning(policy_document)

#!/bin/python3
import configparser
import logging
import os
import random
import sys

import boto3


logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_bucket_options():
    path_to_bucket_dir = os.path.join(BASE_DIR, "buckets")
    files = [
        f
        for f in os.listdir(path_to_bucket_dir)
        if os.path.isfile(os.path.join(path_to_bucket_dir, f))
    ]
    options = list([(f"{i:03d}", filename) for i, filename in enumerate(files)])
    return dict(options)


def delete_bucket(bucket):
    path_to_file = os.path.join(BASE_DIR, "buckets", bucket)
    bucketname = bucket.split(".txt")[0]
    config = configparser.RawConfigParser()
    config.read(path_to_file)

    username = config[bucketname]["AWS_USERNAME"]
    access_key_id = config[bucketname]["AWS_ACCESS_KEY_ID"]
    bucket_name = config[bucketname]["AWS_S3_BUCKET_NAME"]
    policy_arn = config[bucketname]["POLICY_ARN"]

    IAM, S3 = boto3.resource("iam"), boto3.resource("s3")

    policy = IAM.Policy(policy_arn)
    access_key = IAM.AccessKey(username, access_key_id)
    user = IAM.User(username)
    bucket = S3.Bucket(bucket_name)

    logger.warning(f' 1. detaching policy: {policy.policy_name}')
    user.detach_policy(PolicyArn=policy_arn)
    logger.warning(f' 2. deleting policy: {policy.policy_name}')
    policy.delete()
    logger.warning(f' 3. deleting access key: {access_key.id}')
    access_key.delete()
    logger.warning(f' 4. deleting user: {user}')
    user.delete()
    logger.warning(f' 5. deleting bucket: {bucketname}')
    bucket.delete()


if __name__ == "__main__":
    choice = None
    bucket_options = get_bucket_options()
    logger.warning(f"Select which bucket you'd like to delete")
    for opt, bucket in bucket_options.items():
        logger.warning(f" [{opt}] - {bucket}")

    while choice is None:
        b = input(" ↠ which bucket would you like to delete? ")
        if b not in bucket_options.keys():
            choice = None
        else:
            choice = b
    delete_bucket(bucket_options[choice])

    sys.exit()
    IAM, S3 = boto3.client("iam"), boto3.client("s3")

# S3 Utils

Some python scripts to automate the creation of a bucket and a user that can access it. It makes use of the files in the [`words`](./words) directory to give the bucket those cool names like heroku apps (i.e. `prime-rabbit-c6a293d3`).

run `make` to see a list of commands.

## Utilities

### make bucket: create a bucket

1. Generate a name
2. make a bucket with that name
3. make a use with the name plus a `--user` suffix.
4. attach a policy to that user that gives it full access to to bucket.
5. save details about the user and their credentials, the policy, and the bucket to a file `./buckets/<name>.txt`.

### make delete: delete a bucket

1. asks which bucket you'd like to delete.
2. delete bucket, user, and policy

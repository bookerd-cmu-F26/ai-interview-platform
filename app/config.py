import os
AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
USERS_TABLE_NAME = os.getenv("USERS_TABLE_NAME", "Users")
USERS_EMAIL_INDEX_NAME = os.getenv(
 "USERS_EMAIL_INDEX_NAME",
 "email-index",
)
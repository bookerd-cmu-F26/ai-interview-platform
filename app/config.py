import os

AWS_REGION = os.getenv("AWS_REGION", "us-west-2")

USERS_TABLE_NAME = os.getenv(
    "USERS_TABLE_NAME",
    "users",
)

USERS_EMAIL_INDEX_NAME = os.getenv(
    "USERS_EMAIL_INDEX_NAME",
    "email-index",
)

INTERVIEWS_TABLE_NAME = os.getenv(
    "INTERVIEWS_TABLE_NAME",
    "interviews",
)

INTERVIEWS_USER_INDEX_NAME = os.getenv(
    "INTERVIEWS_USER_INDEX_NAME",
    "user_id-created_at-index",
)

QUESTION_GENERATION_QUEUE_URL = os.getenv(
    "QUESTION_GENERATION_QUEUE_URL",
    "https://sqs.us-west-2.amazonaws.com/038040472479/question-generation-queue",
)

QUESTIONS_TABLE_NAME = os.getenv(
    "QUESTIONS_TABLE_NAME",
    "questions",
)

QUESTIONS_INTERVIEW_INDEX_NAME = os.getenv(
    "QUESTIONS_INTERVIEW_INDEX_NAME",
    "interview_id-question_order-index",
)
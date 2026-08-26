from app.workers.question_generation_consumer import (
    QuestionGenerationConsumer,
)


def main() -> None:
    consumer = QuestionGenerationConsumer()

    print(
        "Question generation worker started."
    )

    while True:
        messages = (
            consumer.sqs_service
            .receive_question_generation_messages()
        )

        for message in messages:
            try:
                consumer.process_message(
                    message
                )
            except Exception as error:
                print(
                    "Failed to process message:",
                    error,
                )


if __name__ == "__main__":
    main()
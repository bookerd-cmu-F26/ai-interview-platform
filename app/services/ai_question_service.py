import json
from datetime import datetime, timezone
from uuid import uuid4

from openai import OpenAI

from app.config import OPENAI_MODEL
from app.models.interview import InterviewResponse
from app.models.question import (
    QuestionResponse,
    QuestionType,
)


class AIQuestionService:
    def __init__(self) -> None:
        self.client = OpenAI()

    def generate_questions(
        self,
        interview: InterviewResponse,
    ) -> list[QuestionResponse]:
        requested_types = [
            interview_type.value
            for interview_type in interview.interview_types
        ]

        prompt = f"""
Generate interview questions for this interview.

Job title:
{interview.job_title}

Job description:
{interview.job_description or "Not provided"}

Interview types:
{requested_types}

Requirements:
- Generate exactly one question for each interview type.
- Return questions in the same order as interview_types.
- CODING must be a coding or algorithm question.
- BEHAVIORAL must be a behavioral interview question.
- SYSTEM_DESIGN must be a system design question.
- Do not include answers.
- Do not include explanations.
- Return valid JSON only.

Return exactly this structure:
{{
  "questions": [
    {{
      "question_type": "CODING",
      "question_text": "..."
    }}
  ]
}}
"""

        response = self.client.responses.create(
            model=OPENAI_MODEL,
            input=prompt,
        )

        result = json.loads(
            response.output_text
        )

        generated_questions = result[
            "questions"
        ]

        if len(generated_questions) != len(
            interview.interview_types
        ):
            raise ValueError(
                "AI returned the wrong number of questions"
            )

        questions = []

        for index, generated in enumerate(
            generated_questions
        ):
            expected_type = (
                interview.interview_types[index].value
            )

            if (
                generated["question_type"]
                != expected_type
            ):
                raise ValueError(
                    "AI returned question types "
                    "in the wrong order"
                )

            questions.append(
                QuestionResponse(
                    question_id=str(uuid4()),
                    interview_id=interview.interview_id,
                    question_type=QuestionType(
                        generated["question_type"]
                    ),
                    question_text=generated[
                        "question_text"
                    ],
                    question_order=index + 1,
                    created_at=datetime.now(
                        timezone.utc
                    ),
                )
            )

        return questions
import pytest
from people_also_ask import google


config = dict(
    test_get_answer=dict(
        text="Who is Ho Chi Minh?"
    ),
    test_get_related_questions=dict(
        text="where is france"
    )
)


def test_get_answer():
    answer = google.get_answer(config["test_get_answer"]["text"])
    assert "response" in answer


def test_get_related_questions():
    related_questions = google.get_related_questions(
        config["test_get_related_questions"]["text"]
    )
    assert len(related_questions) > 0


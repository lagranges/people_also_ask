import unittest
from people_also_ask import google


config = dict(
    test_get_answer=dict(
        text="Who is Ho Chi Minh?"
    ),
    test_get_related_questions=dict(
        text="where is france"
    )
)


class TestGoogle(unittest.TestCase):

    def test_get_answer(self):
        answer = google.get_answer(config["test_get_answer"]["text"])
        self.assertIsNotNone(answer)
        self.assertIsNotNone(answer["response"])

    def test_get_related_questions(self):
        related_questions = google.get_related_questions(
            config["test_get_related_questions"]["text"]
        )
        self.assertIsNotNone(related_questions)
        self.assertTrue(len(related_questions) > 0)


if __name__ == "__main__":
    unittest.main()

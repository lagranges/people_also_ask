#! /usr/bin/env python3
import os
import sys
import time
import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional, Generator

from people_also_ask.tools import retryable
from people_also_ask.parser import (
    extract_related_questions,
    get_featured_snippet_parser,
)
from people_also_ask.exceptions import (
    GoogleSearchRequestFailedError,
    RelatedQuestionParserError,
    FeaturedSnippetParserError
)
from people_also_ask.tools import CallingSemaphore


URL = "https://www.google.com/search"
HEADERS = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    " AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/84.0.4147.135 Safari/537.36"
}
SESSION = requests.Session()
NB_TIMES_RETRY = 3
NB_REQUESTS_LIMIT = os.environ.get(
    "RELATED_QUESTION_NBREQUESTS_LIMIT", 25
)
NB_REQUESTS_DURATION_LIMIT = os.environ.get(
    "RELATED_QUESTION_DURATION_LIMIT", 60  # seconds
)
logging.basicConfig()
semaphore = CallingSemaphore(
    NB_REQUESTS_LIMIT, NB_REQUESTS_DURATION_LIMIT
)


@retryable(3)
def search(keyword: str) -> Optional[BeautifulSoup]:
    """return html parser of google search result"""
    params = {"q": keyword}
    try:
        with semaphore:
            time.sleep(0.5)  # be nice with google :)
            response = SESSION.get(URL, params=params, headers=HEADERS)
    except Exception:
        raise GoogleSearchRequestFailedError(URL, keyword)
    if response.status_code != 200:
        raise GoogleSearchRequestFailedError(URL, keyword)
    return BeautifulSoup(response.text, "html.parser")


def _get_related_questions(text: str) -> List[str]:
    """
    return a list of questions related to text.
    These questions are from search result of text

    :param str text: text to search
    """
    document = search(text)
    if not document:
        return []
    try:
        return extract_related_questions(document)
    except Exception:
        raise RelatedQuestionParserError(text)


def generate_related_questions(text: str) -> Generator[str, None, None]:
    """
    generate the questions related to text,
    these quetions are found recursively

    :param str text: text to search
    """
    questions = set(_get_related_questions(text))
    searched_text = set(text)
    while questions:
        text = questions.pop()
        yield text
        searched_text.add(text)
        questions |= set(_get_related_questions(text))
        questions -= searched_text


def get_related_questions(text: str, max_nb_questions: Optional[int] = None):
    """
    return a number of questions related to text.
    These questions are found recursively.

    :param str text: text to search
    """
    if max_nb_questions is None:
        return _get_related_questions(text)
    nb_question_regenerated = 0
    questions = set()
    for question in generate_related_questions(text):
        if nb_question_regenerated > max_nb_questions:
            break
        questions.add(question)
        nb_question_regenerated += 1
    return list(questions)


def get_answer(question: str) -> Dict[str, Any]:
    """
    return a dictionary as answer for a question.

    :param str question: asked question
    """
    document = search(question)
    related_questions = extract_related_questions(document)
    featured_snippet = get_featured_snippet_parser(
            question, document)
    if not featured_snippet:
        res = dict(
            has_answer=False,
            question=question,
            related_questions=related_questions,
        )
    else:
        res = dict(
            has_answer=True,
            question=question,
            related_questions=related_questions,
        )
        try:
            res.update(featured_snippet.to_dict())
        except Exception:
            raise FeaturedSnippetParserError(question)
    return res


def generate_answer(text: str) -> Generator[dict, None, None]:
    """
    generate answers of questions related to text

    :param str text: text to search
    """
    answer = get_answer(text)
    questions = set(answer["related_questions"])
    searched_text = set(text)
    if answer["has_answer"]:
        yield answer
    while questions:
        text = questions.pop()
        answer = get_answer(text)
        if answer["has_answer"]:
            yield answer
        searched_text.add(text)
        questions |= set(get_answer(text)["related_questions"])
        questions -= searched_text


def get_simple_answer(question: str, depth: bool = False) -> str:
    """
    return a text as summary answer for the question

    :param str question: asked quetion
    :param bool depth: return the answer of first related question
        if no answer found for question
    """
    document = search(question)
    featured_snippet = get_featured_snippet_parser(
            question, document)
    if featured_snippet:
        return featured_snippet.response
    if depth:
        related_questions = get_related_questions(question)
        if not related_questions:
            return ""
        return get_simple_answer(related_questions[0])
    return ""


if __name__ == "__main__":
    from pprint import pprint as print
    print(get_answer(sys.argv[1]))

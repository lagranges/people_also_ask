#! /usr/bin/env python3
import sys
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional, Generator

from people_also_ask.parser import (
    extract_related_questions,
    get_featured_snippet_parser,
)
from people_also_ask.exceptions import (
    RelatedQuestionParserError,
    FeaturedSnippetParserError
)
from people_also_ask.request import get
from people_also_ask.request.session import user_agent


URL = "https://www.google.com/search"


def search(keyword: str, url: str = URL) -> Optional[BeautifulSoup]:
    """return html parser of google search result"""
    browser = user_agent['browser']
    params = {"client": browser,
              "q": keyword,
              "sourceid": browser,
              "ie": "UTF-8",
              "oe": "UTF-8"}

    response = get(url, params=params)

    return BeautifulSoup(response.text, "html.parser")


def _get_related_questions(text: str, domain: str="com") -> List[str]:
    """
    return a list of questions related to text.
    These questions are from search result of text

    :param str text: text to search
    :param str domain: specify google domain to improve searching in a native language
    """

    url = f"https://www.google.{domain}/search"
    document = search(text, url=url)
    if not document:
        return []
    try:
        return extract_related_questions(document)
    except Exception:
        raise RelatedQuestionParserError(text)


def generate_related_questions(text: str, domain: str="com") -> Generator[str, None, None]:
    """
    generate the questions related to text,
    these quetions are found recursively

    :param str text: text to search
    :param str domain: specify google domain to improve searching in a native language
    """
    questions = set(_get_related_questions(text, domain=domain))
    searched_text = set(text)
    while questions:
        text = questions.pop()
        yield text
        searched_text.add(text)
        questions |= set(_get_related_questions(text, domain=domain))
        questions -= searched_text


def get_related_questions(text: str, max_nb_questions: Optional[int] = None, domain: str="com"):
    """
    return a number of questions related to text.
    These questions are found recursively.

    :param str text: text to search
    :param str domain: specify google domain to improve searching in a native language
    """
    if max_nb_questions is None:
        return _get_related_questions(text, domain=domain)
    nb_question_regenerated = 0
    questions = []
    for question in generate_related_questions(text, domain=domain):
        if len(set(questions)) >= max_nb_questions:
            break
        questions.append(question)
        nb_question_regenerated += 1

    return list(OrderedDict.fromkeys(questions))
    return list(questions)


def get_answer(question: str, domain: str="com") -> Dict[str, Any]:
    """
    return a dictionary as answer for a question.

    :param str question: asked question
    :param str domain: specify google domain to improve searching in a native language
    """

    url = f"https://www.google.{domain}/search"
    document = search(question, url=url)
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


def generate_answer(text: str, domain: str="com", enhance_search=True) -> Generator[dict, None, None]:
    """
    generate answers of questions related to text

    :param str text: text to search
    :param str domain: specify google domain to improve searching in a native language
    """
    if enhance_search:
        tries = 0
        answer = {"link": False}
    
        while not answer["link"] and tries < 4:
            answer = get_answer(text, domain)
            tries += 1
    else:
        answer = get_answer(text, domain)
     
    questions = set(answer["related_questions"])
    searched_text = set(text)
    if answer["has_answer"]:
        yield answer
    while questions:
        text = questions.pop()
        answer = get_answer(text, domain)
        if answer["has_answer"]:
            yield answer
        searched_text.add(text)
        questions |= set(get_answer(text, domain)["related_questions"])
        questions -= searched_text


def get_simple_answer(question: str, depth: bool = False, domain: str="com") -> str:
    """
    return a text as summary answer for the question

    :param str question: asked quetion
    :param bool depth: return the answer of first related question
        if no answer found for question
    :param str domain: specify google domain to improve searching in a native language
    """

    url = f"https://www.google.{domain}/search"
    document = search(question, url=url)
    featured_snippet = get_featured_snippet_parser(
            question, document)
    if featured_snippet:
        return featured_snippet.response
    if depth:
        related_questions = get_related_questions(question)
        if not related_questions:
            return ""
        return get_simple_answer(related_questions[0], domain)
    return ""


if __name__ == "__main__":
    from pprint import pprint as print
    print(get_answer(sys.argv[1]))

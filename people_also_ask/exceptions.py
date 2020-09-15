#! /usr/bin/env python3
"""
Global realted-questions exception and warning classes.
"""


GITHUB_LINK = "https://github.com/lagranges/people_also_ask"


class RelatedQuestionError(Exception):
    """Base Related-Questions exception class."""

    def __init__(self, error):
        self.error = error

    def __unicode__(self):
        return (
            f'An unkown error occured: {self.error}.'
            f' Please report it on {GITHUB_LINK}.'
        )


class FeaturedSnippetParserError(RelatedQuestionError):
    """
    Exception raised when failed to get answer from
    search result page
    """

    def __init__(self, text):
        self.keyword = text

    def __unicode__(self):
        return (
            f"Cannot parse result page of '{self.text}'."
            f" It mays due to a format change of result page."
            f' Please report it on {GITHUB_LINK}.'
        )


class RelatedQuestionParserError(RelatedQuestionError):
    """
    Exception raised when failed to get related questions
    from search result page
    """

    def __init__(self, text):
        self.keyword = text

    def __unicode__(self):
        return (
            f"Cannot parse result page of '{self.text}'."
            f" It mays due to a format change of result page."
            f' Please report it on {GITHUB_LINK}.'
        )


class GoogleSearchRequestFailedError(RelatedQuestionError):
    """Exception raised when failed to request search on google"""

    def __init__(self, url, keyword):
        self.url = url
        self.keyword = keyword

    def __unicode__(self):
        return (
            f"Failed to requests {self.url}/{self.keyword}"
        )

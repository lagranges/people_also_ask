#! /usr/bin/env python3
"""
Global realted-questions exception and warning classes.
"""


GITHUB_LINK = "https://github.com/lagranges/people_also_ask"


class RelatedQuestionError(Exception):
    """Base Related-Questions exception class."""

    def __init__(self, error):
        self.error = error

    def __repr__(self):
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

    def __repr__(self):
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

    def __repr__(self):
        return (
            f"Cannot parse result page of '{self.text}'."
            f" It mays due to a format change of result page."
            f' Please report it on {GITHUB_LINK}.'
        )


class GoogleSearchRequestFailedError(RelatedQuestionError):
    """Exception raised when failed to request search on google"""

    def __init__(self, url, keyword, message):
        self.url = url
        self.keyword = keyword
        self.message = message

    def __repr__(self):
        return (
            f"Failed to requests {self.url}/{self.keyword}"
            f"\n{self.message}"
        )


class InvalidQuestionInputFileError(RelatedQuestionError):
    """Exception raised when user enter an invalid question input"""
    """ for data collector """

    def __init__(self, input_file, message):
        self.input_file = input_file
        self.message = message

    def __repr__(self):
        return (
            f"Invalid input file: {self.input_file}\n{self.message}"
        )


class FailedToWriteOuputFileError(RelatedQuestionError):
    """Exception raised when program fails to write data to """
    """ output file for data colletor"""

    def __init__(self, output_file, message):
        self.output_file = output_file
        self.message = message

    def __repr__(self):
        return (
            f"Cannot write to {self.output_file}\n{self.message}"
        )


class RequestError(RelatedQuestionError):
    """Exception raised when failed to request"""

    def __init__(self, url, params, proxies, message):
        self.url = url
        self.keyword = params
        self.proxies = proxies
        self.message = message

    def __repr__(self):
        return (
            f"Failed to requests {self.url}"
            f"\nParams = {self.params}"
            f"\nProxy = {self.proxies}"
            f"\nResp = {self.message}"
        )

import os
import unittest
from bs4 import BeautifulSoup
from people_also_ask.parser import (
    get_featured_snippet_parser,
    WholePageTabContainer,
    TableFeaturedSnippetParser,
    YoutubeFeaturedSnippetParser,
    OrderedFeaturedSnippetParser,
    UnorderedFeaturedSnippetParser,
    DefinitionFeaturedSnippetParser,
    MultipleCardsFeaturedSnippetTag,
    SingleCardFeaturedSnippetParser,
)


HTMLS_PARSER = {
    "cheetah_vs_lion.html": YoutubeFeaturedSnippetParser,
    "gangnam_style.html": WholePageTabContainer,
    "how_to_make_a_cold_brew_coffee.html": MultipleCardsFeaturedSnippetTag,
    "the_10_highest-grossing_movies_of_all_time.html": (
        OrderedFeaturedSnippetParser
    ),
    "what_are_3_basic_programming_languages.html": (
        UnorderedFeaturedSnippetParser
    ),
    "what_time_is_it.html": SingleCardFeaturedSnippetParser,
    "why_was_ho_chi_minh_a_hero.html": DefinitionFeaturedSnippetParser,
    "world_university_rankings_2019.html": TableFeaturedSnippetParser
}
FIXTURES_DIR = os.path.join(
    os.path.dirname(__file__),
    "fixtures"
)


class TestParser(unittest.TestCase):

    def test_parsers(self):
        for html_filename, Parser in HTMLS_PARSER.items():
            html_file = os.path.join(FIXTURES_DIR, html_filename)
            with open(html_file, "r") as fd:
                document = BeautifulSoup(fd.read(), "html.parser")
                question, _ = html_filename.split(".")
                question.replace("_", " ")
                parser = get_featured_snippet_parser(question, document)
                self.assertIsInstance(parser, Parser)
                self.assertIsNotNone(parser.response)


if __name__ == "__main__":
    unittest.main()

#! /usr/bin/env python3
from bs4.element import Tag
from bs4 import BeautifulSoup
from operator import attrgetter
from typing import List, Optional
from people_also_ask.tools import itemize, tabulate, remove_redundant


FEATURED_SNIPPET_ATTRIBUTES = [
    "response", "heading", "title", "link", "displayed_link",
    "snippet_str", "snippet_data", "date", "snippet_data",
    "snippet_type", "snippet_str_body", "raw_text"
]


def extract_related_questions(document: BeautifulSoup) -> List[str]:
    div_questions = document.find_all("div", class_="related-question-pair")
    get_text = lambda a: a.text.split('Search for:')[0]
    if not div_questions:
        return []
    questions = list(map(get_text, div_questions))
    return questions


def is_ol_but_not_a_menu(tag):
    return (
        tag.name == "ol"
        and (
            not tag.has_attr("role")
            or (tag.has_attr("role") and tag["role"] != "menu")
            )
        )


def get_tag_heading(tag):
    return (
        tag.find("div", {"role": "heading", "aria-level": "3"})
        or tag.find("div", {"role": "heading"})
    )


def has_youtube_link(tag):
    youtube_links = tag.findAll(
        lambda x: x.name == "a" and "youtube" in x.get("href", "")
    )
    return bool(youtube_links)


def get_raw_text(tag):
    return "\n".join(remove_redundant(tag.strings))


def get_span_text(tag):
    return "\n".join(
            remove_redundant(
                [e.text for e in tag.findAll("span") if e.text]
                )
            )


class FeaturedSnippetParser(object):

    def __init__(self, text: str, tag: Tag):
        self.text = text
        self.tag = tag

    def __getattr__(self, attr):
        if attr in FEATURED_SNIPPET_ATTRIBUTES:
            return None
        raise AttributeError(f'{self.__class__.__name__}.{attr} is invalid.')

    @property
    def raw_text(self):
        return get_raw_text(self.tag)

    def to_dict(self):
        return {
            attr: getattr(self, attr) for attr in FEATURED_SNIPPET_ATTRIBUTES
        }


class SimpleFeaturedSnippetParser(FeaturedSnippetParser):

    @classmethod
    def get_instance(self, text, tag):
        if tag.table is not None:
            return TableFeaturedSnippetParser(text, tag)
        if tag.findAll(is_ol_but_not_a_menu):
            return OrderedFeaturedSnippetParser(text, tag)
        if tag.ul is not None:
            return UnorderedFeaturedSnippetParser(text, tag)
        if get_tag_heading(tag):
            return DefinitionFeaturedSnippetParser(text, tag)
        if has_youtube_link(tag):
            return YoutubeFeaturedSnippetParser(text, tag)

    @property
    def tag_link(self):
        if hasattr(self, "_tag_link"):
            return self._tag_link
        self._tag_link = self.tag.find(
            lambda tag: (
                tag.name == "a"
                and tag.has_attr("href")
                and tag["href"].startswith("http")
                and (tag.h3 or tag.h2) is not None
            )
        )
        return self._tag_link

    @property
    def link(self):
        return self.tag_link["href"] if self.tag_link else None

    @property
    def displayed_link(self):
        return self.tag.cite.text if self.tag.cite else None

    @property
    def title(self):
        if self.tag_link is None:
            return None
        tag_title = self.tag_link.h3 or self.tag_link.h2
        return tag_title.text

    @property
    def heading(self):
        tag_heading = get_tag_heading(self.tag)
        return tag_heading.text

    @property
    def snippet_str(self):
        lines = []
        for field in (
            "heading", "snippet_str_body",
            "displayed_link", "link", "title"
        ):
            if getattr(self, field):
                lines.append(getattr(self, field))
        return "\n".join(lines)

    @property
    def date(self):
        return None

    @property
    def snippet_data(self):
        return None

    @property
    def snippet_type(self):
        return "Unknown Featured Snippet"

    @property
    def snippet_str_body(self):
        return ""


class TableFeaturedSnippetParser(SimpleFeaturedSnippetParser):
    """Example: world university rankings 2019"""

    @property
    def snippet_type(self):
        return "Table Featured Snippet"

    @property
    def snippet_str_body(self):
        header = self.snippet_data["columns"]
        table = self.snippet_data["values"]
        return tabulate(header=header, table=table)

    @property
    def response(self):
        return self.snippet_str_body

    @property
    def snippet_data(self):
        table_tag = self.tag.find("table")
        tr_tags = table_tag.findAll("tr")
        if tr_tags[0].find("th"):
            columns = [
                th_tag.text for th_tag in tr_tags[0].findAll("th")
            ]
            body_table_tags = tr_tags[1:]
        else:
            columns = None
            body_table_tags = tr_tags
        values = [
            [td_tag.text for td_tag in tr_tag.findAll("td")]
            for tr_tag in body_table_tags
        ]
        if columns is None:
            columns = list(range(len(values[0])))
        return {
            "columns": columns,
            "values": values
        }


class OrderedFeaturedSnippetParser(SimpleFeaturedSnippetParser):
    """Example: top grossing movies"""

    @property
    def snippet_type(self):
        return "Ordered Featured Snippet"

    @property
    def response(self):
        return self.snippet_str_body

    @property
    def snippet_str_body(self):
        return "\n".join(itemize(self.snippet_data))

    @property
    def snippet_data(self):
        ol_tags = self.tag.find("ol")
        li_tags = ol_tags.findAll("li")
        return [tag.text for tag in li_tags]


class UnorderedFeaturedSnippetParser(SimpleFeaturedSnippetParser):
    """ What are 3 basic programming languages? """

    @property
    def snippet_type(self):
        return "Unordered Featured Snippet"

    @property
    def snippet_str_body(self):
        return "\n".join(itemize(self.snippet_data))

    @property
    def response(self):
        return self.snippet_str_body

    @property
    def snippet_data(self):
        ul_tag = self.tag.find("ul")
        li_tags = ul_tag.findAll("li")
        return [tag.text for tag in li_tags]


class DefinitionFeaturedSnippetParser(SimpleFeaturedSnippetParser):
    """Why was ho chi minh a hero"""

    @property
    def snippet_type(self):
        return "Definition Featured Snippet"

    @property
    def response(self):
        return self.heading


class YoutubeFeaturedSnippetParser(SimpleFeaturedSnippetParser):
    """Ex: cheetah vs lion"""

    @property
    def snippet_type(self):
        return "Youtube Featured Snippet"

    @property
    def heading(self):
        return ""

    @property
    def response(self):
        return self.link


class MultipleCardsFeaturedSnippetTag(FeaturedSnippetParser):
    """How to make a cold brew coffee"""

    @property
    def heading(self):
        tag_heading = (
            self.tag.find("h3", {"role": "heading"})
            or self.tag.find("h2", {"role": "heading"})
        )
        return tag_heading.text

    @property
    def snippet_type(self):
        return "Multiple Cards Featured Snippet Tag"

    def parse_card(self, tag_card):
        return {
            "heading": tag_card.find("div", {"role": "heading"}).text,
            "title": tag_card.cite.text,
            "link": tag_card.a["href"],
            "raw_text": get_raw_text(tag_card),
        }

    def str_card(self, card_data):
        lines = [card_data["raw_text"]]
        lines.append(f"Link: {card_data['link']}")
        return "\n".join(lines)

    @property
    def snippet_str(self):
        if not self.snippet_data:
            return ""
        return "\n-------------\n".join(map(self.str_card, self.snippet_data))

    @property
    def snippet_data(self):
        return list(map(self.parse_card, self.tag.findAll("g-inner-card")))

    @property
    def response(self):
        return self.snippet_str


class SingleCardFeaturedSnippetParser(FeaturedSnippetParser):
    """What time is it"""

    @property
    def snippet_type(self):
        return "Single Card FeaturedSnippet"

    @property
    def heading(self):
        tag_heading = get_tag_heading(self.tag)
        return get_raw_text(tag_heading)

    @property
    def response(self):
        heading = self.heading
        if heading:
            return heading
        return self.raw_text

    @property
    def raw_text(self):
        return get_span_text(self.tag)


class WholePageTabContainer(FeaturedSnippetParser):
    """Gangnam Style"""

    @property
    def snippet_type(self):
        return "Whole Page Tab Container"

    @property
    def tag_link(self):
        if hasattr(self, "_tag_link"):
            return self._tag_link
        self._tag_link = self.tag.find(
            lambda tag: (
                tag.name == "a"
                and tag.has_attr("href")
                and tag["href"].startswith("http")
                and (tag.h3 or tag.h2) is not None
            )
        )
        return self._tag_link

    @property
    def link(self):
        return self.tag_link["href"] if self.tag_link else None

    @property
    def displayed_link(self):
        return self.tag.cite.text if self.tag.cite else None

    @property
    def title(self):
        if self.tag_link is None:
            return None
        tag_title = self.tag_link.h3 or self.tag_link.h2
        return tag_title.text

    @property
    def response(self):
        return self.raw_text

    @property
    def raw_text(self):
        return get_span_text(self.tag)


def is_simple_featured_snippet_tag(tag):
    class_tuple = tuple(tag.get("class", ""))
    is_xpdopen = (tag.name == "div" and class_tuple == ("xpdopen",))
    if not is_xpdopen:
        return False
    is_xpdopen_of_related_questions = (
        tag.h2 is not None and tag.h2.text == "People also ask"
    )
    return not is_xpdopen_of_related_questions


def is_single_card_featured_snippet_tag(tag):
    is_card_section = (
        tag.name == "div" and "card-section" in tag.get("class", [])
    )
    if not is_card_section:
        return False
    is_card_section_of_tip = tag.text.startswith("Tip:")
    return not is_card_section_of_tip


def is_multiple_card_snippet_tag(tag):
    return (tag.name == "g-section-with-header")


def is_whole_page_tabs_container(tag):
    return (tag.get("id") == "wp-tabs-container")


def is_web_results(tag):
    return (tag.name == "h2" and tag.text == "Web results")


def get_featured_snippet_tag(document):

    def lookup_featured_snippet_tag(tag):
        return (
            is_simple_featured_snippet_tag(tag)
            or is_single_card_featured_snippet_tag(tag)
            or is_multiple_card_snippet_tag(tag)
            or is_web_results(tag)
        )
    whole_page_tag = document.find(is_whole_page_tabs_container)
    tag = document.find(lookup_featured_snippet_tag)
    if tag and is_simple_featured_snippet_tag(tag):
        return tag
    if whole_page_tag:
        return whole_page_tag
    if not tag or tag.name == "h2":
        return None
    return tag


def get_featured_snippet_parser(question, document: BeautifulSoup):
    tag = get_featured_snippet_tag(document)
    if tag is None:
        return
    if is_simple_featured_snippet_tag(tag):
        return SimpleFeaturedSnippetParser.get_instance(question, tag)
    if is_multiple_card_snippet_tag(tag):
        return MultipleCardsFeaturedSnippetTag(question, tag)
    if is_single_card_featured_snippet_tag(tag):
        return SingleCardFeaturedSnippetParser(question, tag)
    if is_whole_page_tabs_container(tag):
        return WholePageTabContainer(question, tag)

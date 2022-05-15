import people_also_ask as paa
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


NB_QUESTION = 10


def generate_article(title: str):
    questions = paa.get_related_questions(title, max_nb_questions=NB_QUESTION)

    introduction = paa.get_simple_answer(title)

    contents = {}
    for question in questions:
        contents[question] = paa.get_simple_answer(question)

    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)

    cur_dir = Path(__file__).parent
    template_path = cur_dir / "templates" / "base.html"
    template = env.from_string(template_path.read_text())

    output = template.render(
        title=title,
        introduction=introduction,
        contents=contents,
        get_question_id=lambda x: x.replace(" ", "_")
    )
    with open("article.html", "w") as fd:
        fd.write(output)
#! /usr/bin/env python3
import time
import json
import argparse
import traceback
from collections import OrderedDict
from people_also_ask.google import get_simple_answer
from people_also_ask.exceptions import (
    InvalidQuestionInputFileError,
    FailedToWriteOuputFileError,
)

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--input-file", "-i", help="input file which is a txt file containing list of questions", required=True)
    parser.add_argument("--output-file", "-o", help="output file which is .json file containing a dictionnary of question: answer", required=True)
    parser.add_argument("--proxy-file", "-p", help="proxy file containing list of proxy")

    return parser.parse_args()


def read_questions(input_file):
    try:
        with open(input_file, "r") as fd:
            text = fd.read()
            return OrderedDict.fromkeys(text.strip().split("\n")).keys()
    except Exception:
        message = traceback.format_exc()
        raise InvalidQuestionInputFileError(input_file, message)

def write_question_answers(output_file, data):
    try:
        with open(output_file, "w") as fd:
            fd.write(json.dumps(data))
    except Exception:
        message = traceback.format_exc()
        raise FailedToWriteOuputFileError(output_file, message)


def collect_one_question(question):
    try:
        answer = get_simple_answer(question)
        print(f"{question}: {answer}")
    except Exception:
        traceback.print_exc()
        answer = ""
    return {question: answer}


def collect_data(input_file, output_file, proxy_file=None):
    questions = read_questions(input_file)
    nb_questions = len(questions)
    counter = 0
    data = {}
    start_time = time.time()
    end_time = None
    if proxy_file is None:
        for question in questions:
            counter += 1
            print(f"COLLECTING {counter}/{nb_questions}")
            data.update(collect_one_question(question))
    end_time = time.time()
    collect_time = (end_time - start_time) / 60  #  minutes
    print(
        f"Collected answers for {nb_questions} questions in {collect_time} minutes"
        )
    write_question_answers(output_file, data)

def main():
    args = parse_args()
    collect_data(args.input_file, args.output_file, args.proxy_file)


if __name__ == "__main__":
    main()

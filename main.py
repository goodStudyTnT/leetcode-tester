import threading
from requests import Session
from helper.utils import get_weekly_contest_tag, open_page, \
    get_weekly_contest_id
from model.problem import Problem
from typing import List
from helper.utils import modify_default_code
from helper.fetch import login, fetch_problem_urls


def open_problems_page(problems: List[Problem]):
    for p in problems:
        if p.openURL:
            open_page(p.url)


def handle_one_problem(session: Session, p: Problem):
    p.parseHTML(session)
    p.default_code = modify_default_code(p.default_code, p.functions, [])

    p.create_dir()

    p.write_main_file()

    p.write_test_file()


def handle_problems(session: Session, problems: List[Problem]):
    # Open Page
    t = threading.Thread(target=open_problems_page, args=(problems,))
    t.start()

    for p in problems:
        print(p.id, p.url)
        t = threading.Thread(target=handle_one_problem,
                             args=(session, p,))
        t.start()


if __name__ == "__main__":
    s = login("goodstudyqaq", "woshiGS#3#")
    contest_id = get_weekly_contest_id(-1)
    file_location = "./leetcode"
    problems = fetch_problem_urls(s, contest_id, file_location)
    handle_problems(s, problems)

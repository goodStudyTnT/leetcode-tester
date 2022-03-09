import shutil
import os
import threading
from requests import Session
from helper.utils import open_page, \
    get_weekly_contest_id
from model.problem import Problem
from model.config import Config
from typing import List
from helper.fetch import login, fetch_problem_urls
from bs4 import BeautifulSoup
import yaml


class Handler(object):

    def __init__(self, config: Config):
        # load config
        self.config = config
        self.parser = None
        self.creator = None

    def _parseHTML(self, session: Session, problem: Problem):
        resp = session.get(problem.url)
        if not resp.ok:
            raise Exception(f"GET {problem.url} return code {resp.status_code}")
        soup = BeautifulSoup(resp.content, "html5lib")

        # 1. 拿到问题基本属性
        problem.default_code, problem.class_name, problem.is_func_problem, problem.functions = self.parser.get_basic_info(
            soup.body_node)

        # 2. 拿到输入输出
        problem.sample_ins, problem.sample_outs = self.parser.get_sample(soup.body_node)

    def create_dir(self, p: Problem):

        try:
            os.makedirs(f"{self.config.contest_dir}/{self.contest_id}/{p.id}")
        except:
            pass
        try:
            os.makedirs(f"{self.config.contest_dir}/utils/cpp")
        except:
            pass
        try:
            if not os.path.exists(
                    f"{self.config.contest_dir}/utils/cpp/help.h"):  # 当不存在时才 copy
                shutil.copyfile("./template/cpp/help.h",
                                f"{self.config.contest_dir}/utils/cpp/help.h")
        except:
            pass

    def handle_one_problem(self, s: Session, p: Problem):
        self._parseHTML(s, p)

        self.create_dir(p)

        self.write_test_file(f"{self.config.contest_dir}/{self.contest_id}/{p.id}/data", p.sample_ins, p.sample_outs)
        self.creator.create_main_code(f"{self.config.contest_dir}/{self.contest_id}/{p.id}/solution.h", p.default_code)
        self.creator.create_test_code(f"{self.config.contest_dir}/{self.contest_id}/{p.id}/data", p)  # 需要传一个路径进去

    def open_problems_page(self, problems: List[Problem]):
        for p in problems:
            if p.openURL:
                open_page(p.url)

    def handle_problems(self, session: Session, problems: List[Problem]):
        # Open Page
        t = threading.Thread(target=self.open_problems_page, args=(problems,))
        t.start()

        for p in problems:
            print(p.id, p.url)
            t = threading.Thread(target=self.handle_one_problem, args=(session, p,))
            t.start()

    def work(self):
        s = login(self.config.username, self.config.password)
        self.contest_id = get_weekly_contest_id(self.config.contest_id)
        problems = fetch_problem_urls(s, self.contest_id)
        self.handle_problems(s, problems)


if __name__ == "__main__":
    with open('./config/weekly_contest.yaml', 'r') as f:
        config = yaml.load(f, yaml.FullLoader)
    config = Config(**config)
    handler = Handler(config)
    handler.work()

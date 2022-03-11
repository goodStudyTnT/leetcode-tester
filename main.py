import argparse
from creator import creator_factory
from parsers import parser_factory
from dacite import from_dict
import json
import dataclasses
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
        self.creator = creator_factory[self.config.language](f"{self.config.current_dir}/template/cpp")
        self.parser = parser_factory[self.config.contest_type](self.creator)

    def _parseHTML(self, session: Session, problem: Problem):
        resp = session.get(problem.url)
        if not resp.ok:
            raise Exception(f"GET {problem.url} return code {resp.status_code}")
        soup = BeautifulSoup(resp.content, "html5lib")
        body_node = soup.body

        problem.language = self.config.language

        # 1. 拿到问题基本属性
        problem.default_code, problem.class_name, problem.is_func_problem, problem.functions = self.parser.get_basic_info(
            body_node)

        # 2. 拿到输入输出
        problem.sample_ins, problem.sample_outs = self.parser.get_sample(body_node, problem.is_func_problem)

    def _write_config(self, file_location: str, p: Problem):
        sample_ins = p.sample_ins
        sample_outs = p.sample_outs
        sample_len = len(sample_ins)
        with open(f"{file_location}/data", "w") as f:
            for i in range(sample_len):
                inputs = sample_ins[i]
                for input in inputs:
                    f.write(input + "\n")
                outputs = sample_outs[i]
                for output in outputs:
                    f.write(output + "\n")

        info = json.dumps(dataclasses.asdict(p), indent=4, sort_keys=True)
        with open(f"{file_location}/problem.json", "w") as f:
            f.write(info)

    def _handle_one_problem(self, s: Session, p: Problem):
        self._parseHTML(s, p)

        directory_location = f"{self.config.contest_dir}/{self.contest_id}/{p.id}/"
        self.creator.create_dir(directory_location)
        self._write_config(directory_location, p)
        self.creator.create_main_code(directory_location, p.default_code)
        self.creator.create_test_code(directory_location, p)  # 需要传一个路径进去

    def _open_problems_page(self, problems: List[Problem]):
        for p in problems:
            if p.openURL:
                open_page(p.url)

    def _handle_problems(self, session: Session, problems: List[Problem]):
        # Open Page
        t = threading.Thread(target=self._open_problems_page, args=(problems,))
        t.start()

        for p in problems:
            print(p.id, p.url)
            t = threading.Thread(target=self._handle_one_problem, args=(session, p,))
            t.start()

    def work(self):
        try:
            s = login(self.config.username, self.config.password)
            self.contest_id = get_weekly_contest_id(self.config.contest_id)
            problems = fetch_problem_urls(s, self.contest_id, self.config.openURL)
            self._handle_problems(s, problems)
            print(f"生成 contest {self.contest_id} 完毕！")
        except Exception as e:
            print(f"生成 contest {self.contest_id} 失败，错误原因：{str(e)}")


def configure(argv):
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    parser_get = subparsers.add_parser("get", help="Download contest problems and generate testing code")
    parser_get.add_argument('--username', type=str, help='Username in leetcode-cn.com')
    parser_get.add_argument('--password', type=str, help='Password in leetcode-cn.com')
    parser_get.add_argument('--language', type=str, help='Programming language. Now support cpp')
    parser_get.add_argument('--contest_dir', type=str, help='Generated code storage location')
    parser_get.add_argument('--contest_id', type=int,
                        help='Contest id. 0: The first upcoming games <0: Previous games >0: Specify contest id')
    parser_get.add_argument('--contest_type', type=str, help='Contest type. Now support weekly')
    parser_get.add_argument('--openURL', type=bool, help='Whether open problem page in browser')

    parser_build = subparsers.add_parser("build_test", help="Build new test based on data file")

    args = parser.parse_args(argv)
    return args


def main(argv=None):
    import os
    location = os.path.abspath(__file__)
    location = os.path.dirname(location)
    args = configure(argv)
    if args.command == "get":
        contest_yaml = os.path.join(location, "config", "config.yaml")
        with open(contest_yaml, 'r') as f:
            config = yaml.load(f, yaml.FullLoader)
            keys = config.keys()
        config["current_dir"] = location
        config = Config(**config)
        print(config)

        for key in keys:
            if hasattr(args, key):
                val = getattr(args, key)
                if val:
                    setattr(config, key, val)

        handler = Handler(config)
        handler.work()
    else:
        current_dir = os.getcwd()
        tmp = os.path.join(current_dir, "problem.json")
        if os.path.exists(tmp):
            with open(tmp, "r") as f:
                p = json.load(f)
                p = from_dict(Problem, p)
            language = p.language
            template_loc = os.path.join(location, "template", language)
            creator = creator_factory[language](template_loc)
            creator.create_test_code(f'{current_dir}/', p)
            print("done!")
        else:
            raise Exception("请在题目路径下执行此命令！")



if __name__ == "__main__":
    exit(main())

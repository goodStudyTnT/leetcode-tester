# coding: utf-8
import json
from dataclasses import dataclass, fields
from typing import List, Optional
from collections import namedtuple
from requests import Session
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from dacite import from_dict


@dataclass
class CodeDefinition(object):
    value: str
    defaultCode: str


@dataclass
class Contest(object):
    id: int
    origin_start_time: int
    start_time: int
    title: str


@dataclass
class Question(object):
    credit: int
    title: str
    title_slug: str


@dataclass
class ContestAPIResponse(object):
    contest: Contest
    questions: List[Question]
    registered: bool
    user_num: int


@dataclass
class Problem(object):
    id: str = None
    url: str = None
    openURL: bool = None

    default_code: str = None
    func_name: str = None
    is_func_problem: bool = None
    func_los: List[int] = None
    custom_comment: str = None

    sample_ins: List[List[str]] = None
    sample_outs: List[List[str]] = None

    contest_dir: str = None

    @classmethod
    def have_children(cls, o):
        try:
            _ = next(o.children)
            return True
        except:
            return False

    def write_to_file(self, content):
        with open("./b", "w") as f:
            f.write(content)

    def parseHTML(self, session: Session):
        resp = session.get(self.url)
        if not resp.ok:
            raise Exception(f"GET {self.url} return code {resp.status_code}")

        soup = BeautifulSoup(resp.content, "html5lib")

        if self.id == "0":
            body_node: Tag = soup.body
            children_iter = body_node.children
            o = next(children_iter)
            while o is not None:
                if o.name == "script" and self.have_children(o):
                    first_child = next(o.children)
                    js_text: NavigableString = first_child.string
                    start = js_text.find("codeDefinition:")
                    if start != -1:
                        end = js_text.find("enableTestMode")
                        json_text = js_text[start + len("codeDefinition:"): end]
                        json_text = json_text.strip()
                        json_text = json_text[:len(json_text) - 3] + "]"
                        json_text = json_text.replace("'", '"', -1)
                        all_code_definition = json.loads(json_text)
                        print(all_code_definition)
                        for code_definition in all_code_definition:
                            cd = from_dict(CodeDefinition, code_definition)
                            # if cd.value == "C++":
                            #     cd.defaultCode =
                o = o.next_sibling

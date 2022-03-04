# coding: utf-8
import json
from dataclasses import dataclass, field
from typing import List
from requests import Session
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from dacite import from_dict
from utils import find_non_ASCII


@dataclass
class CodeDefinition(object):
    value: str
    defaultCode: str


@dataclass
class Problem(object):
    id: str = ""
    url: str = ""
    openURL: bool = False

    default_code: str = ""
    func_name: str = ""
    is_func_problem: bool = False
    func_los: List[int] = field(default_factory=lambda: [])
    custom_comment: str = ""

    sample_ins: List[List[str]] = field(default_factory=lambda: [])
    sample_outs: List[List[str]] = field(default_factory=lambda: [])

    contest_dir: str = ""

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

    # 细分的话有四种题目类型：
    # 函数 - 无预定义类型，绝大多数题目都是这个类型
    # 函数 - 有预定义类型，如 LC174C
    # 方法 - 无预定义类型，如 LC175C
    # 方法 - 有预定义类型，如 LC163B
    def parse_golang_code(self, code):
        lines = code.split("\n")
        if "func Constructor(" in code:
            func_los = []
            for lo, line in enumerate(lines):
                if line.startswith("func Constructor("):
                    func_los.append(lo)
                elif line.startswith("func ("):
                    func_los.append(lo)
            func_name = "Constructor"
            return func_name, False, func_los
        else:
            for lo, line in enumerate(lines):
                if line.startswith("func "):
                    i = line.find("(")
                    return line[5:i].strip(), True, [lo]

    def parse_sample_text(self, text: str, parse_args: bool):
        text = text.strip()
        if text == "":
            return []
        lines = text.split("\n")
        for i, s in enumerate(lines):
            lines[i] = s.strip()

        # 由于新版的样例不是这种格式了，这种特殊情况就不处理了
        # 见 https://leetcode-cn.com/contest/weekly-contest-121/problems/time-based-key-value-store/
        if not self.is_func_problem:
            return lines

        text = "".join(lines)
        idx = find_non_ASCII(text)
        if idx != -1:
            print("[warn] 样例数据含有非 ASCII 字符，截断，原文为", text)
            text = text[:idx]

        # 不含等号，说明只有一个参数
        if not parse_args or "=" not in text:
            return [text]

        # TODO: 处理参数本身含有 = 的情况
        splits = text.split("=")
        sample = []
        for s in splits[1: len(splits) - 1]:
            end = s.rfind(",")
            sample.append(s[:end].strip())
        sample.append(splits[len(splits) - 1].strip())
        if not self.is_func_problem:
            sample = ["\n".join(sample) + "\n"]
        return sample

    def parse_node(self, o: Tag):
        # 提取并解析每个 <pre> 块内的文本（以中文为基准解析）
        # 需要判断 <pre> 的下一个子元素是否为 tag
        #     https://leetcode-cn.com/contest/weekly-contest-190/problems/max-dot-product-of-two-subsequences/
        #     https://leetcode-cn.com/contest/weekly-contest-212/problems/arithmetic-subarrays/
        # 有 tag 也不一定为 <strong>
        #     <img> https://leetcode-cn.com/contest/weekly-contest-103/problems/snakes-and-ladders/
        #     <b> https://leetcode-cn.com/contest/weekly-contest-210/problems/split-two-strings-to-make-palindrome/
        # 提取出文本后，去掉「解释」和「提示」后面的文字，然后分「输入」和「输出」来解析后面的数据
        if o.name == "pre" and self.have_children(o):
            children_iter = o.children
            first_child = next(children_iter)
            if first_child.name != "img" and first_child.name != "image":
                data = first_child.string
                data = data.strip()
                if data.startswith("输"):  # 输入(极少情况下会错误地写成输出)
                    raw_data = []

                    def parse_pre_node(o: Tag):
                        if o.name is None:
                            raw_data.append(str(o.string))
                        if self.have_children(o):
                            children_iter = o.children
                            c = next(children_iter)
                            while c is not None:
                                parse_pre_node(c)
                                c = c.next_sibling

                    parse_pre_node(o)
                    raw_data = "".join(raw_data)

                    i = raw_data.find("解")
                    if i >= 0:
                        raw_data = raw_data[:i]
                    i = raw_data.find("提")
                    if i >= 0:
                        raw_data = raw_data[:i]
                    raw_data = raw_data.strip()
                    raw_data = raw_data[3:]  # 去掉 输入：
                    i = raw_data.find("输")
                    self.sample_ins.append(
                        self.parse_sample_text(raw_data[:i], True))

                    raw_data = raw_data[i + 3:]  # 去掉 输出：
                    self.sample_outs.append(
                        self.parse_sample_text(raw_data, True))

        if self.have_children(o):
            children_iter = o.children
            c = next(children_iter)
            while c is not None:
                self.parse_node(c)
                c = c.next_sibling

    def parse_special_node(self, o: Tag):
        if o.name == "div" and self.have_children(o):
            children_iter = o.children
            first_child = next(children_iter)
            raw: str = first_child.string
            sp = raw.split("`")
            for i, s in enumerate(sp):
                if ">输入" in s or "> 输入" in s:
                    text = sp[i + 1]
                    if not self.is_func_problem:
                        # https://leetcode-cn.com/contest/season/2020-fall/problems/IQvJ9i/
                        text += "\n" + sp[i + 3]
                    self.sample_ins.append(self.parse_sample_text(text, True))
                elif ">输出" in s or "> 输出" in s:
                    self.sample_outs.append(
                        self.parse_sample_text(sp[i + 1], True))

        if self.have_children(o):
            children_iter = o.children
            c = next(children_iter)
            while c is not None:
                self.parse_special_node(c)
                c = c.next_sibling

    def parseHTML(self, session: Session):
        resp = session.get(self.url)
        if not resp.ok:
            raise Exception(f"GET {self.url} return code {resp.status_code}")

        soup = BeautifulSoup(resp.content, "html5lib")

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
                        if cd.value == "golang":
                            self.default_code = cd.defaultCode.strip()
                            self.func_name, self.is_func_problem, self.func_los = self.parse_golang_code(
                                self.default_code)
            o = o.next_sibling

        if self.default_code == "":
            raise Exception("解析失败 未找到 GO 代码模板!")

        self.parse_node(body_node)

        if len(self.sample_ins) == 0:
            # 没找到 <pre> 国服特殊比赛(春秋赛等)
            self.parse_special_node(body_node)

        if len(self.sample_ins) != len(self.sample_outs):
            raise Exception(
                "len(sampleIns) != len(sampleOuts) : %d != %d" % (
                    len(self.sample_ins), len(self.sample_outs)))
        if len(self.sample_ins) == 0:
            raise Exception("解析失败，未找到样例输入输出！")

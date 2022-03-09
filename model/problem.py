# coding: utf-8
import json
import shutil
import os
from dataclasses import dataclass, field
from typing import List
from requests import Session
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from dacite import from_dict
from helper.utils import find_non_ASCII, get_first_children
from string import Template


@dataclass
class CodeDefinition(object):
    value: str
    defaultCode: str


@dataclass
class Function(object):
    name: str = ""
    location: int = 0
    is_constructor: bool = True  # 是否是构造函数
    output_params: str = ""  # 出参
    input_params: List[str] = field(default_factory=lambda: [])  # 入参


@dataclass
class Problem(object):
    id: str = ""
    url: str = ""
    openURL: bool = False

    default_code: str = ""
    is_func_problem: bool = True
    class_name: str = ""
    functions: List[Function] = field(default_factory=lambda: [])
    sample_ins: List[List[str]] = field(default_factory=lambda: [])
    sample_outs: List[List[str]] = field(default_factory=lambda: [])

    def write_main_file(self):
        file_location = f"{self.contest_dir}/{self.contest_id}/{self.id}/solution.h"

        d = {
            "custom_comment": "test",
            "problem": self.default_code
        }

        with open("./template/cpp/solve.h", "r") as f:
            src = Template(f.read())
            result = src.substitute(d)

        with open(file_location, "w") as f:
            f.writelines(result)

    def convert_input_for_cpp(self, input_type, input):
        input = str(input)
        input = input.replace("'", "")
        input = input.replace("[", "{")
        input = input.replace("]", "}")
        input = input.replace("null", "NULL")

        print(input_type, input)

        # 特判 TreeNode* + ListNode*
        if "TreeNode" in input_type or "ListNode" in input_type:
            keyword = "TreeNode" if "TreeNode" in input_type else "ListNode"
            # 找到包围数字的 { }
            # 有可能是 vector<vector<TreeNode*>> -》 {{{1, 2, 3}, {4, 5, 6}}, {{9, 9, 9}, {8, 9, 10}}}
            brackets = []
            need_update = []
            for idx, c in enumerate(input):
                if c == '{':
                    brackets.append((idx, c))
                elif c == '}':
                    if brackets[-1][1] == '{':  # 是包围的
                        left_idx = brackets[-1][0]
                        need_update.append((left_idx, idx))
                    brackets.append((idx, c))

            update_idx = 0
            real_input = ""
            for idx, c in enumerate(input):
                if update_idx < len(need_update):
                    if idx == need_update[update_idx][0]:
                        real_input += f"new {keyword}(" + c
                    elif idx == need_update[update_idx][1]:
                        real_input += f"{c})"
                        update_idx += 1
                    else:
                        real_input += c
                else:
                    real_input += c
            input = real_input
        return input

    def build_params(self, input_type, input_name, input_val):
        number = len(input_val)
        input_val = self.convert_input_for_cpp(input_type, input_val)

        # 去掉引用符号
        input_type = input_type.replace("&", "")
        res = f"{input_type} {input_name}[{number}] = {input_val};"
        return res

    def build_test(self):
        res = {}
        test_num = len(self.sample_ins)
        res["test_num"] = test_num
        if self.is_func_problem:
            # 是函数 则在最开始的时候就实例化一个类
            # 一般来说只有一个函数
            # todo: 待验证
            f = self.functions[0]
            begin = [f"{self.class_name} sol = {self.class_name}();"]
            result_str = self.build_params(f.output_params, "res",
                                           self.sample_outs)
            begin.append(result_str)
            # 得到所有参数的 name 和 type
            input_names = []
            for idx, input_param in enumerate(f.input_params):
                tmp = input_param.split(" ")
                input_type = tmp[0]
                input_name = tmp[1]
                input_names.append(f"{input_name}[i]")
                vals = [val[idx] for val in self.sample_ins]
                result_str = self.build_params(input_type, input_name, vals)
                begin.append(result_str)

            # 构造 for 循环里的内容
            test = []
            input_names_str = ", ".join(input_names)
            test.append(
                f"{f.output_params} my_ans = sol.{f.name}({input_names_str});")
            test.append(f"compare_result(i, my_ans, res[i]);")
            begin = [f"\t{val}" for val in begin]
            begin_str = "\n".join(begin)
            test = [f"\t\t{val}" for val in test]
            test_str = "\n".join(test)
            res["begin"] = begin_str
            res["test"] = test_str
        else:
            pass
        return res

    def write_test_file(self):
        file_location = f"{self.contest_dir}/{self.contest_id}/{self.id}/main.cpp"
        d = self.build_test()

        with open("./template/cpp/main.cpp", "r") as f:
            src = Template(f.read())
            result = src.substitute(d)

        with open(file_location, "w") as f:
            f.writelines(result)



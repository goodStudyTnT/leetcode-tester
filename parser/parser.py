from typing import List
from model.problem import Function
from bs4 import Tag
from creator.creator import CodeCreator
from helper.utils import find_non_ASCII


class Parser(object):

    def __init__(self, creator: CodeCreator):
        self.creator = creator

    def parse_sample_text(self, text: str, parse_args: bool):
        text = text.strip()
        if text == "":
            return []
        lines = text.split("\n")
        for i, s in enumerate(lines):
            lines[i] = s.strip()

        text = "".join(lines)
        idx = find_non_ASCII(text)
        if idx != -1:
            print("[warn] 样例数据含有非 ASCII 字符，截断，原文为", text)
            text = text[:idx]

        # 不含等号，说明只有一个参数
        if not parse_args or "=" not in text:
            return text

        # TODO: 处理参数本身含有 = 的情况
        splits = text.split("=")
        print(splits)
        sample = []
        for s in splits[1: len(splits) - 1]:
            end = s.rfind(",")
            sample.append(s[:end].strip())
        sample.append(splits[len(splits) - 1].strip())
        return sample

    def get_basic_info(self, node: Tag) -> (str, str, bool, List[Function]):
        """
        Get problem's basic info by parse HTML
        :param node: body node
        :return:
        Tuple(default_code, class_name, is_func_problem, functions)
        """

    def get_sample(self, node: Tag) -> (List[List[str]], List[List[str]]):
        """
        Get problem's sample inputs and outputs by parse HTML
        :param node: body node
        :return:
        Tuple(sample_ins, sample_outs)
        """

from parsers.parser import Parser
from typing import List
from model.problem import Function
from bs4 import Tag
from creator.creator import CodeCreator
from helper.utils import get_first_children


# todo: 待验证
class SeasonContestParser(Parser):

    contest_type = "season"

    def get_basic_info(self, node: Tag) -> (str, str, bool, List[Function]):
        pass

    def get_sample(self, node: Tag) -> (List[List[str]], List[List[str]]):
        sample_ins = []
        sample_outs = []

        def work(o):
            first_child = get_first_children(o)
            if o.name == "div" and first_child:
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
                        sample_ins.append(self.parse_sample_text(text, True))
                    elif ">输出" in s or "> 输出" in s:
                        sample_outs.append(
                            self.parse_sample_text(sp[i + 1], True))

            c = get_first_children(o)
            while c is not None:
                work(c)
                c = c.next_sibling

        work(node)
        if len(sample_ins) != len(sample_outs):
            raise Exception("len(sampleIns) != len(sampleOuts) : %d != %d" % (len(sample_ins), len(sample_outs)))
        if len(sample_ins) == 0:
            raise Exception("解析失败，未找到样例输入输出！")

        return sample_ins, sample_outs

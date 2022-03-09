from parser.parser import Parser
from typing import List
from model.problem import Function
from bs4 import Tag, NavigableString
from helper.utils import get_first_children
import json
from dacite import from_dict
from model.problem import CodeDefinition


class WeeklyContestParser(Parser):
    def get_basic_info(self, node: Tag) -> (str, str, bool, List[Function]):
        default_code = ""
        class_name = ""
        is_func_problem = True
        functions = []

        o = get_first_children(node)
        while o is not None:
            first_child = get_first_children(o)
            if o.name == "script" and first_child:
                js_text: NavigableString = first_child.string
                start = js_text.find("codeDefinition:")
                if start != -1:
                    end = js_text.find("enableTestMode")
                    json_text = js_text[start + len("codeDefinition:"): end]
                    json_text = json_text.strip()
                    json_text = json_text[:len(json_text) - 3] + "]"
                    json_text = json_text.replace("'", '"', -1)
                    all_code_definition = json.loads(json_text)
                    for code_definition in all_code_definition:
                        cd = from_dict(CodeDefinition, code_definition)
                        cd.defaultCode = cd.defaultCode.strip()
                        if cd.value == self.creator.code_type:
                            default_code = cd.defaultCode
                            class_name, is_func_problem, functions = self.creator.parse_code(default_code)
                            break
            o = o.next_sibling

        if default_code == "":
            raise Exception(f"解析失败 未找到 {self.creator.code_type} 代码模板!")

        return default_code, class_name, is_func_problem, functions


    def get_sample(self, node: Tag) -> (List[List[str]], List[List[str]]):
        # 提取并解析每个 <pre> 块内的文本（以中文为基准解析）
        # 需要判断 <pre> 的下一个子元素是否为 tag
        #     https://leetcode-cn.com/contest/weekly-contest-190/problems/max-dot-product-of-two-subsequences/
        #     https://leetcode-cn.com/contest/weekly-contest-212/problems/arithmetic-subarrays/
        # 有 tag 也不一定为 <strong>
        #     <img> https://leetcode-cn.com/contest/weekly-contest-103/problems/snakes-and-ladders/
        #     <b> https://leetcode-cn.com/contest/weekly-contest-210/problems/split-two-strings-to-make-palindrome/
        # 提取出文本后，去掉「解释」和「提示」后面的文字，然后分「输入」和「输出」来解析后面的数据
        sample_ins = []
        sample_outs = []

        def work(o):
            first_child = get_first_children(node)
            if o.name == "pre" and first_child:
                if first_child.name != "img" and first_child.name != "image":
                    data = first_child.string
                    data = data.strip()
                    if data.startswith("输"):  # 输入(极少情况下会错误地写成输出)
                        raw_data = []

                        def parse_pre_node(o: Tag):
                            if o.name is None:
                                raw_data.append(str(o.string))
                            c = get_first_children(o)
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
                        sample_ins.append(self.parse_sample_text(raw_data[:i], True))

                        raw_data = raw_data[i + 3:]  # 去掉 输出：
                        sample_outs.append(self.parse_sample_text(raw_data, True))

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

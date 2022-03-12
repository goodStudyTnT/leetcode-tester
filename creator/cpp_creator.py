from collections import defaultdict
from creator.creator import CodeCreator
from model.problem import Function, Problem
import os
import shutil
from string import Template
from helper.utils import convert_str_to_list


class CppCreator(CodeCreator):
    code_type = "cpp"

    def create_dir(self, dir_loc):
        os.makedirs(dir_loc, exist_ok=True)
        os.makedirs(f"{dir_loc}/../../utils/cpp", exist_ok=True)
        if not os.path.exists(f"{dir_loc}/../../utils/cpp/help.h"):  # 当不存在时才 copy
            shutil.copyfile(f"{self._template_dir}/help.h", f"{dir_loc}/../../utils/cpp/help.h")

    def parse_code(self, code):
        lines = code.split("\n")
        # get class name
        class_name = ""
        for l in lines:
            i = l.find("class")
            if i != -1:
                class_name = l[6:-2]
                break
        functions = list()
        is_func_problem = True
        for lo, line in enumerate(lines):
            line = line.strip()
            if "{" in line and not line.startswith("struct") and not line.startswith("class") and not line.startswith("/*") and not line.startswith("//") and not line.startswith("*"):
                f = Function()
                i = line.find("(")
                left = line[:i]
                right = line[i + 1:]
                left_words = left.split(" ")
                f.name = left_words[-1].strip()
                f.is_constructor = (f.name == class_name)
                if f.is_constructor:
                    is_func_problem = False
                f.location = lo
                name_len = len(f.name)
                f.output_params = left[:-name_len - 1].strip()
                i = right.find(")")
                right = right[:i]
                right_words = right.split(",")
                for w in right_words:
                    w = w.strip()
                    f.input_params.append(w)
                functions.append(f)
        return class_name, is_func_problem, functions

    def create_main_code(self, dir_loc, code, custom_comment):
        file_location = f"{dir_loc}/solution.h"
        d = {
            "custom_comment": custom_comment,
            "problem": code,
        }

        with open(f"{self._template_dir}/solve.h", "r") as f:
            src = Template(f.read())
            result = src.substitute(d)

        with open(file_location, "w") as f:
            f.writelines(result)

    def _convert_input_for_cpp(self, input_type, input):
        input = str(input)
        input = input.replace("'", "")
        input = input.replace("[", "{")
        input = input.replace("]", "}")
        input = input.replace("null", "NULL")

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

    def _build_params(self, input_type, input_name, input_val):
        number = len(input_val)
        input_val = self._convert_input_for_cpp(input_type, input_val)

        # 去掉引用符号
        input_type = input_type.replace("&", "")
        res = f"{input_type} {input_name}[{number}] = {input_val};"
        return res

    def _build_test(self, sample_ins, sample_outs, p: Problem):
        res = {}
        test_num = len(sample_ins)
        res["test_num"] = test_num
        if p.is_func_problem:
            # 是函数 则在最开始的时候就实例化一个类
            # 一般来说只有一个函数
            # todo: 待验证
            f = p.functions[0]
            begin = [f"{p.class_name} sol = {p.class_name}();"]
            vals = [val[0] for val in sample_outs]
            result_str = self._build_params(f.output_params, "res",
                                            vals)
            begin.append(result_str)
            # 得到所有参数的 name 和 type
            input_names = []
            for idx, input_param in enumerate(f.input_params):
                tmp = input_param.split(" ")
                input_type = tmp[0]
                input_name = tmp[1]
                input_names.append(f"{input_name}[i]")
                vals = [val[idx] for val in sample_ins]
                result_str = self._build_params(input_type, input_name, vals)
                begin.append(result_str)

            # 构造 for 循环里的内容
            test = []
            input_names_str = ", ".join(input_names)
            test.append(
                f"{f.output_params} my_ans = sol.{f.name}({input_names_str});")
            test.append(f'compare_result(to_string(i), my_ans, res[i]);')
            begin = [f"    {val}" for val in begin]
            begin_str = "\n".join(begin)
            test = [f"        {val}" for val in test]
            test_str = "\n".join(test)
            res["begin"] = begin_str
            res["test"] = test_str
        else:
            pass
        return res

    def _create_func_problem_test(self, dir_loc, p: Problem):
        # 输入 输出 从 data 里面读
        data_location = f"{dir_loc}/data"
        sample_ins = []
        sample_outs = []

        sample_in_len = len(p.functions[0].input_params)
        sample_out_len = 1

        with open(data_location, "r") as f:
            lines = f.read().splitlines()
            lines = [line.strip() for line in lines]
            # lines = f.readlines()
            now = 0
            while now < len(lines):
                go = now
                ins = []
                outs = []
                while go < len(lines) and len(ins) < sample_in_len:
                    if lines[go] != "\n" and lines[go] != "":
                        ins.append(lines[go])
                    go += 1
                while go < len(lines) and len(outs) < sample_out_len:
                    if lines[go] != '\n' and lines[go] != "":
                        outs.append(lines[go])
                    go += 1
                if len(ins) != sample_in_len or len(outs) != sample_out_len:
                    raise Exception(f" 题目 {p.id} 样例文件 data 错误，请检查! ins={ins} outs={outs}")

                sample_ins.append(ins)
                sample_outs.append(outs)
                now = go

        file_location = f"{dir_loc}/main.cpp"
        d = self._build_test(sample_ins, sample_outs, p)

        with open(f"{self._template_dir}/main.cpp", "r") as f:
            src = Template(f.read())
            result = src.substitute(d)

        with open(file_location, "w") as f:
            f.writelines(result)

    def _build_method_test(self, sample_methods, sample_ins, sample_outs, p: Problem):
        res = {}
        test_num = len(sample_methods)

        name_to_function = {}

        for f in p.functions:
            name_to_function[f.name] = f
        begin = []
        for idx in range(test_num):
            methods = sample_methods[idx]
            ins = sample_ins[idx]
            outs = sample_outs[idx]
            begin.append(f"void test{idx}(){{")
            methods = convert_str_to_list(methods, 2)
            ins = convert_str_to_list(ins, 2)
            outs = convert_str_to_list(outs, 2)

            params = set()
            names = set()
            name_to_val = defaultdict(list)

            for idx2, method in enumerate(methods):
                methods[idx2] = method[1:-1]  # 去掉引号
                method = methods[idx2]
                f = name_to_function[method]
                input_params = f.input_params
                for idx3, p in enumerate(input_params):
                    if p == "":
                        continue
                    tmp = p.split(" ")
                    input_type = tmp[0]
                    input_name = tmp[1]

                    key = f"{method}_{input_name}"

                    if key in params:
                        # 在里面
                        name_to_val[key].append(ins[idx2][idx3])
                    elif input_name in names:
                        i = 0
                        while f"{input_name}{i}" in names:
                            i += 1
                        input_name = f"{input_name}{i}"
                        name_to_function[method].input_params[idx3] = f"{input_type} {input_name}"
                        names.add(input_name)
                        key = f"{method}_{input_name}"
                        params.add(key)
                        name_to_val[key].append(ins[idx2][idx3])
                    else:
                        names.add(input_name)
                        key = f"{method}_{input_name}"
                        params.add(key)
                        name_to_val[key].append(ins[idx2][idx3])

            for f in name_to_function.values():
                for input_param in f.input_params:
                    if input_param == "":
                        continue
                    tmp = input_param.split(" ")
                    input_type = tmp[0]
                    input_name = tmp[1]
                    key = f"{f.name}_{input_name}"
                    result_str = self._build_params(input_type, input_name, name_to_val[key])
                    begin.append(f"    {result_str}")

            name_to_idx = defaultdict(int)
            return_num = 0
            for idx2, method in enumerate(methods):
                f = name_to_function[method]
                input = []
                for p in f.input_params:
                    if p == "":
                        continue
                    tmp = p.split(" ")
                    input_name = tmp[1]
                    key = f"{method}_{input_name}"
                    the_idx = name_to_idx[key]
                    name_to_idx[key] += 1
                    input.append(f"{input_name}[{the_idx}]")

                input_str = ", ".join(input)
                result = outs[idx2]
                if idx2 == 0:
                    # 构造函数
                    begin.append(f"    {method} *obj = new {method}({input_str});")
                else:
                    # 判断是否有 return
                    have_return = (result != "null")
                    if have_return:
                        output_type = f.output_params

                        begin.append(f"    {output_type} res{return_num} = obj->{method}({input_str});")
                        begin.append(f"    {output_type} ans{return_num} = {result};")
                        begin.append(f"    compare_result(\"{idx}-{return_num}\", res{return_num}, ans{return_num});")
                        return_num += 1
                    else:
                        begin.append(f"    obj->{method}({input_str});")
            begin.append("}")

        begin_str = "\n".join(begin)

        test = []
        for idx in range(test_num):
            test.append(f"test{idx}();")
        test = [f"    {val}" for val in test]
        test_str = "\n".join(test)

        res["begin"] = begin_str
        res["test"] = test_str
        return res

    def _create_method_problem_test(self, dir_loc, p: Problem):
        # 输入 输出 从 data 里面读
        data_location = f"{dir_loc}/data"
        sample_methods = []
        sample_ins = []
        sample_outs = []

        with open(data_location, "r") as f:
            lines = f.read().splitlines()
            lines = [line.strip() for line in lines]
            now = 0
            while now < len(lines):
                go = now
                methods = None
                ins = None
                outs = None
                while go < len(lines) and methods is None:
                    if lines[go] != "\n" and lines[go] != "":
                        methods = lines[go]
                    go += 1
                while go < len(lines) and ins is None:
                    if lines[go] != "\n" and lines[go] != "":
                        ins = lines[go]
                    go += 1

                while go < len(lines) and outs is None:
                    if lines[go] != "\n" and lines[go] != "":
                        outs = lines[go]
                    go += 1
                if methods is None or ins is None or outs is None:
                    raise Exception(f"题目 {p.id} 样例文件 data 错误，请检查!")
                sample_methods.append(methods)
                sample_ins.append(ins)
                sample_outs.append(outs)

                now = go

        file_location = f"{dir_loc}/main.cpp"
        d = self._build_method_test(sample_methods, sample_ins, sample_outs, p)

        with open(f"{self._template_dir}/method_main.cpp", "r") as f:
            src = Template(f.read())
            result = src.substitute(d)

        with open(file_location, "w") as f:
            f.writelines(result)

    def create_test_code(self, dir_loc, p: Problem):
        if p.is_func_problem:
            self._create_func_problem_test(dir_loc, p)
        else:
            self._create_method_problem_test(dir_loc, p)

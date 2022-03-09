from creator.creator import CodeCreator
from model.problem import Function


class CppCreator(CodeCreator):
    code_type = "cpp"

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
            if "{" in line and "struct" not in line and "class" not in line and \
                    line[1] != "*":
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

from creator.creator import CodeCreator


class GolangCreator(CodeCreator):
    code_type = "golang"

    def parse_code(self, code):
        # 细分的话有四种题目类型：
        # 函数 - 无预定义类型，绝大多数题目都是这个类型
        # 函数 - 有预定义类型，如 LC174C
        # 方法 - 无预定义类型，如 LC175C
        # 方法 - 有预定义类型，如 LC163B
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

# coding: utf-8
from dataclasses import dataclass, field
from typing import List


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

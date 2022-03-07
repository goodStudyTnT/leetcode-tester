import datetime
import webbrowser
from typing import List


def get_weekly_contest_id(contest_id=0):
    if contest_id <= 0:
        end_time_170 = datetime.datetime(2020, 1, 5, 12, 0, 0,
                                         0)  # The 170's leetcode weekly contest end time in China(utc-8)
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        week_since_170 = 1 + int(
            (now - end_time_170) / datetime.timedelta(hours=7 * 24))
        contest_id += week_since_170 + 170
    return contest_id


def get_biweekly_contest_id(contest_id=0):
    if contest_id <= 0:
        end_time_17 = datetime.datetime(2020, 1, 12, 0, 0, 0,
                                        0)  # The 17's leetcode biweekly contest end time in China(utc-8)
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=8)
        two_week_since_17 = 1 + int(
            (now - end_time_17) / datetime.timedelta(hours=2 * 7 * 24))
        contest_id += 17 + two_week_since_17
    return contest_id


def get_weekly_contest_tag(contest_id=0):
    return f"weekly-contest-{str(get_weekly_contest_id(contest_id))}"


def get_biweekly_contest_tag(contest_id=0):
    return f"biweekly-contest-{str(get_biweekly_contest_id(contest_id))}"


def open_page(url):
    webbrowser.open(url)


def find_non_ASCII(s):
    for i in s:
        if 0 <= ord(i) <= 127:
            continue
        else:
            return i
    return -1


def parse_return_type(line):
    i = line.find(")")
    print("lll", line)
    return line[i + 1: len(line) - 2].strip()


def modify_default_code(code: str, func_los: List[int], func_list: List,
                        custom_func_content: str):
    sep = "\n"
    if "\r" in code:
        sep = "\r\n"
    print(code)

    lines = code.split(sep)
    for lo in func_los:
        tp = parse_return_type(lines[lo])
        if tp == "int64":
            custom_func_content = "\tans := 0\n" + custom_func_content + " int64(ans)"
            lines[lo + 1] = custom_func_content
        for f in func_list:
            lines[lo] = f(lines[lo])

    res = sep.join(lines)
    print(res)

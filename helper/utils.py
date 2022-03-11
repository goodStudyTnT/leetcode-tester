import datetime
import webbrowser


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
    return line[i + 1: len(line) - 2].strip()


def get_first_children(o):
    try:
        c = next(o.children)
        return c
    except:
        return None


def convert_str_to_list(s: str, dep: int):
    # 将 str 转成 list 大于 dep 的深度则不转
    # [1, 2, 3, [4, 5]]
    def work(s, now_dep):
        res = []
        now = 1
        while now < len(s) - 1:  # 去掉 []
            if now_dep < dep and s[now] == '[':
                go = now
                score = 0
                while go < len(s) - 1:
                    if s[go] == '[':
                        score += 1
                    elif s[go] == ']':
                        score -= 1
                    go += 1
                    if score == 0:
                        val = work(s[now: go], now_dep + 1)
                        res.append(val)
                        break
                now = go + 1 # 逗号
                if now < len(s) - 1 and s[now] == " ":
                    now += 1
            else:
                val = ""
                go = now
                # 应该不会有字符串里面有逗号吧？
                while go < len(s) - 1 and s[go] != ",":
                    val += s[go]
                    go += 1
                res.append(val)
                now = go + 1  # s[go] = ','
                if now < len(s) - 1 and s[now] == " ":
                    now += 1
        print(res)
        return res

    return work(s, 0)

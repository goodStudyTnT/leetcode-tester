import json
import threading
import time

from dacite import from_dict

import requests
from requests import Session
from utils import get_weekly_contest_tag, open_page
from model.contest import ContestAPIResponse
from model.problem import Problem
from typing import List
from utils import modify_default_code

host = "leetcode-cn.com"


# 使用用户名和密码登录
def login(username, password):
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
    s = requests.Session()
    s.headers.update({"user-agent": ua})
    csrf_token_url = f"https://{host}/graphql/"
    resp = s.post(csrf_token_url, json={
        "operationName": "globalData",
        "query": "query globalData {\n  feature {\n    questionTranslation\n    subscription\n    signUp\n    discuss\n    mockInterview\n    contest\n    store\n    book\n    chinaProblemDiscuss\n    socialProviders\n    studentFooter\n    cnJobs\n    __typename\n  }\n  userStatus {\n    isSignedIn\n    isAdmin\n    isStaff\n    isSuperuser\n    isTranslator\n    isPremium\n    isVerified\n    isPhoneVerified\n    isWechatVerified\n    checkedInToday\n    username\n    realName\n    userSlug\n    groups\n    jobsCompany {\n      nameSlug\n      logo\n      description\n      name\n      legalName\n      isVerified\n      permissions {\n        canInviteUsers\n        canInviteAllSite\n        leftInviteTimes\n        maxVisibleExploredUser\n        __typename\n      }\n      __typename\n    }\n    avatar\n    optedIn\n    requestRegion\n    region\n    activeSessionId\n    permissions\n    notificationStatus {\n      lastModified\n      numUnread\n      __typename\n    }\n    completedFeatureGuides\n    useTranslation\n    __typename\n  }\n  siteRegion\n  chinaHost\n  websocketUrl\n}\n",
    })

    if not resp.ok:
        raise Exception(f"POST {csrf_token_url} return code {resp.status_code}")

    csrf_token = ""
    for c in resp.cookies:
        if c.name == "csrftoken":
            csrf_token = c.value
            break

    if csrf_token == "":
        raise Exception("csrftoken not found in response")

    # log in
    login_url = f"https://{host}/accounts/login/"
    resp = s.post(login_url, data={
        "csrfmiddlewaretoken": csrf_token,
        "login": username,
        "password": password,
        "next": "/",
    }, headers={
        "origin": f"https://{host}",
        "referer": f"https://{host}/"
    })
    if not resp.ok:
        raise Exception(f"POST {login_url} return code {resp.status_code}")

    if s.cookies.get("LEETCODE_SESSION") is None:
        raise Exception("登录失败：账号或密码错误")

    return s


def fetch_problem_urls(session: Session, contest_tag):
    contest_info_url = f"https://{host}/contest/api/info/{contest_tag}"
    resp = session.get(contest_info_url)
    if not resp.ok:
        raise Exception(
            f"POST {contest_info_url} return code {resp.status_code}")

    try:
        d = from_dict(ContestAPIResponse, resp.json())
    except Exception as e:
        raise e

    if d.contest.start_time == 0:
        raise Exception(f"未找到比赛或比赛尚未开始: {contest_tag}")

    sleep_time = d.contest.start_time - int(time.time())  # unix time
    if sleep_time > 0:
        if not d.registered:
            raise Exception(f"该账号尚未报名{d.contest.title}")
        sleep_time += 2
        print(f"{d.contest.title} 尚未开始，请等待 {sleep_time} 秒...")
        time.sleep(sleep_time)
        return fetch_problem_urls(session, contest_tag)

    if len(d.questions) == 0:
        raise Exception(f"题目链接为空 {contest_tag}")

    print("难度 标题")
    for q in d.questions:
        print("%3d %s" % (q.credit, q.title))

    problems = []
    for idx, q in enumerate(d.questions):
        problems.append(Problem(id=str(idx),
                                url=f"https://{host}/contest/{contest_tag}/problems/{q.title_slug}/",
                                is_func_problem=True))
    return problems


def open_problems_page(problems: List[Problem]):
    for p in problems:
        if p.openURL:
            open_page(p.url)


def handle_one_problem(session: Session, p: Problem):
    p.parseHTML(session)

    p.default_code = modify_default_code(p.default_code, p.func_los, [],
                                         "\t\n\treturn")

    # p.create_dir()
    #
    # p.write_main_file()
    #
    # p.write_test_file()


def handle_problems(session: Session, problems: List[Problem]):
    # Open Page
    t = threading.Thread(target=open_problems_page, args=(problems,))
    t.start()

    for p in problems:
        print(p.id, p.url)
        t = threading.Thread(target=handle_one_problem, args=(session, p))
        t.start()


if __name__ == "__main__":
    s = login("goodstudyqaq", "woshiGS#3#")
    problems = fetch_problem_urls(s, get_weekly_contest_tag(-1))
    handle_problems(s, problems)

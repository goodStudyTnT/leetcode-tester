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

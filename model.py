# coding: utf-8
import json
from dataclasses import dataclass, fields, field
from typing import List, Optional
from collections import namedtuple
from requests import Session
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
from dacite import from_dict
from utils import find_non_ASCII



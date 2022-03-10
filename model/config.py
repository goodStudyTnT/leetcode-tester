from dataclasses import dataclass


@dataclass
class Config(object):
    username: str
    password: str
    language: str
    contest_dir: str
    contest_id: int
    contest_type: str

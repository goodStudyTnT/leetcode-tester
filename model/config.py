from dataclasses import dataclass


@dataclass
class Config(object):
    username: str
    password: str
    language: str
    openURL: bool


    contest_dir: str
    contest_id: int
    contest_type: str

    current_dir: str

    custom_comment: str

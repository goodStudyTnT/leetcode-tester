from parsers.weekly_contest_parser import WeeklyContestParser
from parsers.season_contest_parser import SeasonContestParser
parser_factory = {
    WeeklyContestParser.contest_type: WeeklyContestParser,
    "biweekly": WeeklyContestParser,
    SeasonContestParser.contest_type: SeasonContestParser
}

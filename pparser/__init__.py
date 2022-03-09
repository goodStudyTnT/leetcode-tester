from pparser.weekly_contest_parser import WeeklyContestParser
from pparser.season_contest_parser import SeasonContestParser
parser_factory = {
    WeeklyContestParser.contest_type: WeeklyContestParser,
    SeasonContestParser.contest_type: SeasonContestParser
}

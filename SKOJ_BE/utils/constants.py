class Choices:
    @classmethod
    def choices(cls):
        d = cls.__dict__
        return [d[item] for item in d.keys() if not item.startswith("__")]


class ContestType:
    PUBLIC_CONTEST = "Public"
    PASSWORD_PROTECTED_CONTEST = "Password Protected"


class ContestStatus:
    CONTEST_NOT_START = "1"
    CONTEST_ENDED = "-1"
    CONTEST_UNDERWAY = "0"


class ContestRuleType(Choices):
    ACM = "ACM"
    OI = "OI"


class CourseType:
    PUBLIC_COURSE = "Public"
    PASSWORD_PROTECTED_COURSE = "Password Protected"

class CourseStatus:
    COURSE_NOT_START = "1"
    COURSE_ENDED = "-1"
    COURSE_UNDERWAY = "0"

class CacheKey:
    waiting_queue = "waiting_queue"
    contest_rank_cache = "contest_rank_cache"
    website_config = "website_config"


class Difficulty(Choices):
    LOW = "Low"
    MID = "Mid"
    HIGH = "High"

class Type(Choices):
    Radio = 'Radio'
    Check = 'Check'
    True_False = 'True_False'

CONTEST_PASSWORD_SESSION_KEY = "contest_password"
COURSE_PASSWORD_SESSION_KEY = "course_password"
import platform
if platform.system().lower() == 'windows':
    TMP_PATH = "./tmp/"
else:
    TMP_PATH = "/tmp/"
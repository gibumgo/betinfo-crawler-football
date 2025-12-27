# Global Configuration

# Flashscore Settings
FLASHSCORE_BASE_URL = "https://www.flashscore.co.kr"
FLASHSCORE_IMAGE_URL = "https://static.flashscore.com"
DEFAULT_SEASON = "2025-2026"

# Betinfo Settings
BETINFO_BASE_URL = "https://www.betinfo.co.kr"
BETINFO_MATCH_URL = f"{BETINFO_BASE_URL}/z_protorate/protoRate2.asp"

# CLI Defaults
DEFAULT_OUTPUT_DIR = "./data"
DEFAULT_TIMEOUT = 300
DEFAULT_RECENT_COUNT = 5

# Data Directories - Single Source of Truth
DIR_DATA = DEFAULT_OUTPUT_DIR
DIR_DATA_MASTER = f'{DIR_DATA}/master'
DIR_DATA_ALIASES = f'{DIR_DATA}/aliases'
DIR_DATA_CRAWLED_FLASHSCORE = f'{DIR_DATA}/crawled/flashscore'
DIR_DATA_CRAWLED_BETINFO = f'{DIR_DATA}/crawled/betinfo'

# File Paths (Aliases for compatibility or specific usage)
# Master Data
DEFAULT_TEAMS_CSV_PATH = f'{DIR_DATA_MASTER}/teams.csv'
DEFAULT_LEAGUES_CSV_PATH = f'{DIR_DATA_MASTER}/leagues.csv'
LEAGUE_TEAMS_FILENAME = f'{DIR_DATA_MASTER}/league_teams.csv'

# Mappings (Aliases)
DEFAULT_TEAM_ALIAS_JSON_PATH = f'{DIR_DATA_ALIASES}/team_aliases.json'
DEFAULT_LEAGUE_ALIAS_JSON_PATH = f'{DIR_DATA_ALIASES}/league_aliases.json'

# Default Collection Parameters
DEFAULT_NATION = "england"
DEFAULT_LEAGUE_NAME = "premier-league"
DEFAULT_LEAGUE_PATH = "/soccer/england/premier-league/"

# Driver Settings
DRIVER_WAIT_TIME = 20
DRIVER_HEADLESS = True
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# History Settings
HISTORY_FILENAME = "history.json"
MAX_HISTORY_RECORDS = 100

# Flashscore URL Templates
FS_RESULTS_URL_TEMPLATE = "{base_url}/soccer/{nation}/{league}-{season}/results/"
FS_SUMMARY_URL_TEMPLATE = "{base_url}/soccer/{nation}/{league}-{season}/standings/#/{league_id}/standings/overall/"

# Mapping Thresholds
THRESHOLD_AUTO_MATCH = 80
THRESHOLD_CONFIRM_MATCH = 50

# Flashscore File Patterns
FLASHSCORE_MATCH_FILE_PATTERN = "flashscore_matches_*.csv"


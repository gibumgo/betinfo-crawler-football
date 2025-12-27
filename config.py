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

# Data Storage Settings
DATA_DIR = DEFAULT_OUTPUT_DIR
LEAGUES_FILENAME = f"{DATA_DIR}/leagues.csv"
TEAMS_FILENAME = f"{DATA_DIR}/teams.csv"
LEAGUE_TEAMS_FILENAME = f"{DATA_DIR}/league_teams.csv"
MATCHES_FILENAME_TEMPLATE = f"{DATA_DIR}/matches_{{season}}_{{league}}_v1.csv"

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

# Data Directories
DIR_DATA = DEFAULT_OUTPUT_DIR
DIR_DATA_MASTER = f'{DIR_DATA}/master'
DIR_DATA_MAPPINGS = f'{DIR_DATA}/mappings'
DIR_DATA_CRAWLED_FLASHSCORE = f'{DIR_DATA}/crawled/flashscore'
DIR_DATA_CRAWLED_BETINFO = f'{DIR_DATA}/crawled/betinfo'

# Mapping Files
DEFAULT_TEAM_MAPPING_JSON_PATH = f'{DIR_DATA_MAPPINGS}/team_mappings.json'
DEFAULT_LEAGUE_MAPPING_JSON_PATH = f'{DIR_DATA_MAPPINGS}/league_mappings.json'

# Helper alias for compatibility if needed, or prefer using DIR_DATA_MASTER directly
DEFAULT_TEAMS_CSV_PATH = f'{DIR_DATA_MASTER}/teams.csv'
DEFAULT_LEAGUES_CSV_PATH = f'{DIR_DATA_MASTER}/leagues.csv'

# Flashscore File Patterns
FLASHSCORE_MATCH_FILE_PATTERN = "flashscore_matches_*.csv"


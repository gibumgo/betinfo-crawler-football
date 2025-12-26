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


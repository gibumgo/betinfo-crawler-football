
# 로그 메시지 템플릿
MSG_AUTO_MAPPED = "Auto-mapped: {original} -> {matched} ({score:.1f}%)"
MSG_CANDIDATE_HEADER = "\n🤔 '{original}' 매칭 후보를 확인해주세요:"
MSG_CANDIDATE_ITEM = "  [{idx}] {name} (유사도: {score:.1f}%)"
MSG_SKIP_OPTION = "  [0] 건너뛰기 (매칭 안 함)"
MSG_SAVED_SUCCESS = "✅ 저장 완료: {original} -> {matched}"
MSG_BATCH_MODE_SKIP = "Skipping interactive confirmation for '{original}' due to non-interactive mode."
MSG_FILE_NOT_FOUND = "{type} CSV not found at {path}"
MSG_ERROR_LOADING = "Error loading {type} CSV: {error}"

# JSON Keys
JSON_KEY_ALIASES = "aliases"

COL_MATCH_DATETIME = 'match_datetime'
COL_HOME_TEAM = 'home_team_name'
COL_AWAY_TEAM = 'away_team_name'
COL_HOME_ID = 'url_team1_id'
COL_AWAY_ID = 'url_team2_id'

# Teams CSV Configuration
COL_TEAM_ID = 'team_id'
COL_TEAM_NAME_KO = 'team_name_ko'
COL_TEAM_NAME_EN = 'team_name'

# Leagues CSV Configuration
COL_LEAGUE_ID = 'league_id'
COL_LEAGUE_NAME_KO = 'league_name_ko'
COL_LEAGUE_NAME_EN = 'league_name'
COL_LEAGUE_NATION = 'nation'
COL_LEAGUE_NATION_KO = 'nation_ko'

# MatchContextResolver Log Messages
MSG_ERROR_LOADING_FILE = "Error loading {filename}: {error}"
MSG_LOADED_MATCHES_COUNT = "Loaded {count} matches for context resolution"

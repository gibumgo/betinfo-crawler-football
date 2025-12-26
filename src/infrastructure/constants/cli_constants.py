# Argument Names
ARG_MODE = "--mode"
ARG_TASK = "--task"
ARG_RECENT = "--recent"
ARG_ROUNDS = "--rounds"
ARG_START_ROUND = "--start-round"
ARG_END_ROUND = "--end-round"
ARG_OUTPUT_DIR = "--output-dir"
ARG_HEADLESS = "--headless"
ARG_NO_HEADLESS = "--no-headless"
ARG_TIMEOUT = "--timeout"
ARG_DEBUG = "--debug"
ARG_CONFIG = "--config"
ARG_INTERACTIVE = "--interactive"
ARG_YEAR = "--year"

# Flashscore Arguments
ARG_TASK = "--task"
ARG_URL = "--url"
ARG_SEASON = "--season"
ARG_FS_START_ROUND = "--fs-start-round"
ARG_FS_END_ROUND = "--fs-end-round"
ARG_CHECKPOINT_INTERVAL = "--checkpoint-interval"
ARG_RESUME = "--resume"

# Choices
CLI_MODES = ("betinfo", "flashscore")
FLASH_TASKS = ("matches", "metadata")

DEFAULT_INTERACTIVE_NAMESPACE = {
    "interactive": True,
    "mode": None
}

# Help Texts
HELP_MODE = "실행 모드 선택 (필수)"
HELP_HEADLESS = "브라우저 숨김 모드 (기본: {default})"
HELP_NO_HEADLESS = "브라우저 표시 모드"
HELP_OUTPUT_DIR = "데이터 저장 경로 (기본: {default})"
HELP_TIMEOUT = "프로세스 강제 종료 시간 (초, 기본: {default})"
HELP_DEBUG = "디버그 로그 활성화"
HELP_CONFIG = "설정 파일 경로 (선택)"
HELP_INTERACTIVE = "대화형 모드 강제 실행"
HELP_YEAR = "대상 연도 (기본: {default})"

HELP_RECENT = "최신 N개 회차 자동 수집"
HELP_ROUNDS = "특정 회차 목록 (쉼표 구분)"
HELP_START_ROUND = "범위 수집 시작 회차"
HELP_END_ROUND = "범위 수집 종료 회차"

HELP_TASK = "Flashscore 작업 유형"
HELP_URL = "Flashscore 대상 URL"
HELP_SEASON = "시즌 명시 (기본: {default})"
HELP_FS_START_ROUND = "Flashscore 라운드 시작"
HELP_FS_END_ROUND = "Flashscore 라운드 종료"
HELP_CHECKPOINT_INTERVAL = "중간 저장 간격 (0: 비활성)"
HELP_RESUME = "중단 지점부터 재개"

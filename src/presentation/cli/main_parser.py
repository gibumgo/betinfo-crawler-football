import argparse
import sys
import config
from typing import Optional
from infrastructure.constants.cli_constants import (
    ARG_MODE, ARG_HEADLESS, ARG_NO_HEADLESS, ARG_OUTPUT_DIR,
    ARG_TIMEOUT, ARG_DEBUG, ARG_CONFIG, ARG_INTERACTIVE,
    ARG_RECENT, ARG_ROUNDS, ARG_START_ROUND, ARG_END_ROUND,
    ARG_TASK, ARG_URL, ARG_SEASON, ARG_FS_START_ROUND,
    ARG_FS_END_ROUND, ARG_CHECKPOINT_INTERVAL, ARG_RESUME,
    CLI_MODES, FLASH_TASKS, DEFAULT_INTERACTIVE_NAMESPACE,
    HELP_MODE, HELP_HEADLESS, HELP_NO_HEADLESS, HELP_OUTPUT_DIR,
    HELP_TIMEOUT, HELP_DEBUG, HELP_CONFIG, HELP_INTERACTIVE,
    HELP_RECENT, HELP_ROUNDS, HELP_START_ROUND, HELP_END_ROUND,
    HELP_FS_END_ROUND, HELP_CHECKPOINT_INTERVAL, HELP_RESUME,
    ARG_YEAR, HELP_YEAR, ARG_SKIP_EXISTING, HELP_SKIP_EXISTING,
    HELP_TASK, HELP_URL, HELP_SEASON, HELP_FS_START_ROUND
)

class MainParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Betinfo & Flashscore Football Crawler CLI",
            formatter_class=argparse.RawTextHelpFormatter
        )
        self._setup_arguments()

    def _setup_arguments(self):
        self.parser.add_argument(
            ARG_MODE, 
            type=str, 
            choices=CLI_MODES, 
            help=HELP_MODE
        )

        # --- 2. Common Options ---
        self.parser.add_argument(ARG_HEADLESS, action="store_true", default=config.DRIVER_HEADLESS, help=HELP_HEADLESS.format(default=config.DRIVER_HEADLESS))
        self.parser.add_argument(ARG_NO_HEADLESS, action="store_false", dest="headless", help=HELP_NO_HEADLESS)
        
        self.parser.add_argument(ARG_OUTPUT_DIR, type=str, default=config.DIR_DATA, help=HELP_OUTPUT_DIR.format(default=config.DIR_DATA))
        self.parser.add_argument(ARG_TIMEOUT, type=int, default=config.DEFAULT_TIMEOUT, help=HELP_TIMEOUT.format(default=config.DEFAULT_TIMEOUT))
        self.parser.add_argument(ARG_DEBUG, action="store_true", help=HELP_DEBUG)
        self.parser.add_argument(ARG_CONFIG, type=str, help=HELP_CONFIG)
        self.parser.add_argument(ARG_INTERACTIVE, action="store_true", help=HELP_INTERACTIVE)

        # --- 3. Betinfo Options ---
        import datetime
        current_year = datetime.datetime.now().year
        
        betinfo_group = self.parser.add_argument_group("Betinfo Options")
        betinfo_group.add_argument(ARG_YEAR, type=int, default=current_year, help=HELP_YEAR.format(default=current_year))
        betinfo_group.add_argument(ARG_RECENT, type=int, help=HELP_RECENT)
        betinfo_group.add_argument(ARG_ROUNDS, type=str, help=HELP_ROUNDS)
        betinfo_group.add_argument(ARG_START_ROUND, type=str, help=HELP_START_ROUND)
        betinfo_group.add_argument(ARG_END_ROUND, type=str, help=HELP_END_ROUND)
        betinfo_group.add_argument(ARG_SKIP_EXISTING, action="store_true", help=HELP_SKIP_EXISTING)

        flash_group = self.parser.add_argument_group("Flashscore Options")
        flash_group.add_argument(ARG_TASK, type=str, choices=FLASH_TASKS, help=HELP_TASK)
        flash_group.add_argument(ARG_URL, type=str, help=HELP_URL)
        flash_group.add_argument(ARG_SEASON, type=str, default=config.DEFAULT_SEASON, help=HELP_SEASON.format(default=config.DEFAULT_SEASON))
        flash_group.add_argument(ARG_FS_START_ROUND, type=int, help=HELP_FS_START_ROUND)
        flash_group.add_argument(ARG_FS_END_ROUND, type=int, help=HELP_FS_END_ROUND)
        flash_group.add_argument(ARG_CHECKPOINT_INTERVAL, type=int, default=0, help=HELP_CHECKPOINT_INTERVAL)
        flash_group.add_argument(ARG_RESUME, action="store_true", help=HELP_RESUME)

    def parse_args(self) -> argparse.Namespace:
        if len(sys.argv) == 1:
            return argparse.Namespace(**DEFAULT_INTERACTIVE_NAMESPACE)
        return self.parser.parse_args()

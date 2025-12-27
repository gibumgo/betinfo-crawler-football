import os
import glob
import pandas as pd
from datetime import datetime
import config
from shared.ipc_messenger import IPCMessenger
from infrastructure.constants.mapping_constants import (
    COL_MATCH_DATETIME,
    COL_HOME_TEAM,
    COL_AWAY_TEAM,
    COL_HOME_ID,
    COL_AWAY_ID,
    MSG_ERROR_LOADING_FILE,
    MSG_LOADED_MATCHES_COUNT
)

class MatchContextResolver:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.match_index = {}
        self._load_flashscore_matches()

    def _load_flashscore_matches(self):
        pattern = os.path.join(self.data_dir, config.FLASHSCORE_MATCH_FILE_PATTERN)
        files = glob.glob(pattern)
        
        count = 0
        for f in files:
            try:
                df = pd.read_csv(f, dtype=str)
                required = [
                    COL_MATCH_DATETIME, 
                    COL_HOME_TEAM, 
                    COL_AWAY_TEAM, 
                    COL_HOME_ID, 
                    COL_AWAY_ID
                ]
                
                if not all(col in df.columns for col in required):
                    continue
                
                for _, row in df.iterrows():
                    try:
                        dt_str = row[COL_MATCH_DATETIME].split(' ')[0]
                        if dt_str not in self.match_index:
                            self.match_index[dt_str] = []
                        
                        self.match_index[dt_str].append({
                            'home': row[COL_HOME_TEAM],
                            'away': row[COL_AWAY_TEAM],
                            'home_id': row[COL_HOME_ID],
                            'away_id': row[COL_AWAY_ID]
                        })
                        count += 1
                    except Exception:
                        continue
            except Exception as e:
                IPCMessenger.log(MSG_ERROR_LOADING_FILE.format(filename=f, error=e), level="WARN")

        IPCMessenger.log(MSG_LOADED_MATCHES_COUNT.format(count=count), level="INFO")

    def find_potential_match(self, date_str: str, betinfo_home: str, betinfo_away: str):
        target_date = date_str
        if len(date_str) == 8 and date_str.isdigit():
             target_date = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

        candidates = self.match_index.get(target_date, [])
        if not candidates:
            return None

        return candidates

import json
import os
import time
import config
from datetime import datetime
from uuid import uuid4

class HistoryManager:
    def __init__(self, data_dir: str = config.DEFAULT_OUTPUT_DIR):
        self.data_dir = data_dir
        self.history_file = os.path.join(data_dir, config.HISTORY_FILENAME)
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
            
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def start_session(self, mode: str, args: dict) -> str:
        session_id = str(uuid4())
        record = {
            "id": session_id,
            "mode": mode,
            "args": args,
            "status": "RUNNING",
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "log_summary": None,
            "error_message": None
        }
        
        self._append_record(record)
        return session_id

    def end_session(self, session_id: str, status: str, summary: str = None, error: str = None):
        history = self._load_history()
        
        updated = False
        for record in history:
            if record["id"] == session_id:
                record["status"] = status
                record["end_time"] = datetime.now().isoformat()
                record["log_summary"] = summary
                record["error_message"] = error
                updated = True
                break
        
        if updated:
            self._save_history(history)

    def _load_history(self) -> list:
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def _append_record(self, record: dict):
        history = self._load_history()
        history.insert(0, record)
        if len(history) > config.MAX_HISTORY_RECORDS:
            history = history[:config.MAX_HISTORY_RECORDS]
        self._save_history(history)

    def _save_history(self, history: list):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

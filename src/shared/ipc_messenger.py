
import sys
from typing import Any
from infrastructure.constants.ipc_constants import (
    IPC_STATUS, IPC_PROGRESS, IPC_ERROR, IPC_CHECKPOINT, IPC_DATA, IPC_LOG,
    LOG_LEVEL_INFO, LOG_LEVEL_WARN, LOG_LEVEL_ERROR
)

class IPCMessenger:
    @staticmethod
    def send_status(status_type: str, value: Any) -> None:
        print(f"{IPC_STATUS}:{status_type}|{value}", flush=True)

    @staticmethod
    def send_progress(percent: float) -> None:
        print(f"{IPC_PROGRESS}:{percent:.1f}", flush=True)

    @staticmethod
    def send_checkpoint(data: Any) -> None:
        print(f"{IPC_CHECKPOINT}:{data}", flush=True)
        
    @staticmethod
    def send_error(code: int, message: str) -> None:
        print(f"{IPC_ERROR}:{code}|{message}", flush=True)

    @staticmethod
    def log(message: str, level: str = "INFO") -> None:
        try:
            formatted = f"[LOG][{level}] {message}\n"
            sys.stderr.write(formatted)
            sys.stderr.flush()
        except Exception:
            pass
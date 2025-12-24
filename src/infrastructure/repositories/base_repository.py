import pandas as pd
import os
from dataclasses import asdict
from datetime import datetime
from typing import Any

class BaseRepository:
    def __init__(self, column_map: dict[str, str]):
        self.column_map = column_map
    
    def save_to_csv(self, items: list, filename: str) -> None:
        if not items:
            print(f"⚠️ 저장할 데이터가 없습니다: {filename}")
            return
        
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        csv_rows = []
        for item in items:
            data_dict = asdict(item)
            
            data_dict = self._convert_datetime_to_string(data_dict)
            
            mapped_row = {
                self.column_map.get(key, key): value 
                for key, value in data_dict.items()
            }
            csv_rows.append(mapped_row)
        
        dataframe = pd.DataFrame(csv_rows)
        dataframe.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"💾 저장 완료: {filename} ({len(items)}개)")
    
    def _convert_datetime_to_string(self, data_dict: dict) -> dict:
        converted = {}
        for key, value in data_dict.items():
            if isinstance(value, datetime):
                converted[key] = value.strftime("%Y-%m-%d %H:%M")
            else:
                converted[key] = value
        return converted

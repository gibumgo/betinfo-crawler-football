import pandas as pd
import os
from dataclasses import asdict, is_dataclass
from typing import List, Any, Optional

class CsvRepository:
    def save_to_csv(
        self, 
        items: List[Any], 
        filename: str, 
        append: bool = False, 
        deduplicate: bool = False, 
        deduplicate_subset: Optional[List[str]] = None,
        column_map: Optional[dict] = None
    ) -> None:
        if not items:
            return

        new_df = self._prepare_dataframe(items, column_map)
        
        self._ensure_directory(filename)

        if append and os.path.exists(filename):
            self._save_append(new_df, filename, deduplicate, deduplicate_subset)
        else:
            self._save_overwrite(new_df, filename)

    def _prepare_dataframe(self, items: List[Any], column_map: Optional[dict]) -> pd.DataFrame:
        data = self._to_dict_list(items)
        
        if column_map:
            data = [
                {column_map.get(k, k): v for k, v in row.items()}
                for row in data
            ]
            
        return pd.DataFrame(data)

    def _ensure_directory(self, filename: str) -> None:
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)

    def _save_append(self, new_df: pd.DataFrame, filename: str, deduplicate: bool, subset: Optional[List[str]] = None) -> None:
        existing_df = pd.read_csv(filename)
        combined_df = pd.concat([existing_df, new_df])
        
        if deduplicate:
            combined_df.drop_duplicates(subset=subset, inplace=True, keep='last')
        
        combined_df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"✅ [Append] Saved {len(new_df)} items to {filename} (Total: {len(combined_df)})")

    def _save_overwrite(self, new_df: pd.DataFrame, filename: str) -> None:
        new_df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"✅ [Create] Saved {len(new_df)} items to {filename}")

    def _to_dict_list(self, items: List[Any]) -> List[dict]:
        return [self._convert_item_to_dict(item) for item in items]

    def _convert_item_to_dict(self, item: Any) -> dict:
        if hasattr(item, 'model_dump'): 
            return item.model_dump()
        
        if hasattr(item, 'dict'): 
            return item.dict()

        if is_dataclass(item):
            return asdict(item)

        if isinstance(item, dict):
            return item

        return item.__dict__

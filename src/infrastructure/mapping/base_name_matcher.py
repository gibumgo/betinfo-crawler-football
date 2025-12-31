import json
import os
import pandas as pd
from typing import Optional, List, Tuple
from difflib import SequenceMatcher
import config
from shared.ipc_messenger import IPCMessenger
from infrastructure.constants.mapping_constants import (
    MSG_AUTO_MAPPED, MSG_CANDIDATE_HEADER, MSG_CANDIDATE_ITEM,
    MSG_SKIP_OPTION, MSG_SAVED_SUCCESS, MSG_BATCH_MODE_SKIP,
    MSG_FILE_NOT_FOUND, MSG_ERROR_LOADING,
    JSON_KEY_ALIASES
)

class BaseNameMatcher:
    def __init__(self, csv_path: str, json_path: str, entity_type: str):
        self.csv_path = csv_path
        self.json_path = json_path
        self.entity_type = entity_type
        
        self.master_data = self._load_master_data()
        self.learned_mappings = self._load_learned_json()
        
        if not self.learned_mappings and self.master_data:
            self._seed_from_master()
            self.learned_mappings = self._load_learned_json()
            
        self.search_candidates = self._build_search_list()
        
        self.knowledge_base = self._build_knowledge_base()

    def _seed_from_master(self):
        seed_data = {}
        count = 0
        
        for item in self.master_data:
            _id = item.get('league_id') or item.get('team_id') or item.get('id')
            if not _id: continue
            
            aliases = set()
            
            if item.get('league_name'): aliases.add(item['league_name'])
            if item.get('team_name'): aliases.add(item['team_name'])
            if item.get('name'): aliases.add(item['name'])
            
            if item.get('league_name_ko'): aliases.add(item['league_name_ko'])
            if item.get('team_name_ko'): aliases.add(item['team_name_ko'])
            if item.get('name_ko'): aliases.add(item['name_ko'])
            
            nation = item.get('nation')
            nation_ko = item.get('nation_ko')
            
            l_name = item.get('league_name')
            l_name_ko = item.get('league_name_ko')
            
            if nation and l_name:
                aliases.add(f"{nation} {l_name}")
                aliases.add(f"{nation} - {l_name}")
            
            if nation_ko and l_name_ko:
                aliases.add(f"{nation_ko} {l_name_ko}")
                aliases.add(f"{nation_ko} - {l_name_ko}")
                aliases.add(f"{nation_ko}{l_name_ko}")
            
            if aliases:
                valid_aliases = [a.strip() for a in aliases if a and a.strip()]
                if valid_aliases:
                    seed_data[_id] = {JSON_KEY_ALIASES: valid_aliases}
                    count += 1
        
        if seed_data:
            IPCMessenger.log(f"🌱 Seeding {self.entity_type} aliases from master: {count} items", level="INFO")
            try:
                os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
                with open(self.json_path, 'w', encoding='utf-8') as f:
                    json.dump(seed_data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                IPCMessenger.log(f"❌ Failed to seed aliases: {e}", level="ERROR")

    def _build_knowledge_base(self) -> dict:
        kb = {}
        
        for cand in self.search_candidates:
            kb[cand['search_name']] = cand['id']
            
        for alias, lid in self.learned_mappings.items():
            kb[alias] = lid
            
        IPCMessenger.log(f"🧠 Knowledge Base loaded: {len(kb)} entries (Master + Aliases)", level="INFO")
        return kb

    def _load_master_data(self) -> List[dict]:
        if not os.path.exists(self.csv_path):
            IPCMessenger.log(MSG_FILE_NOT_FOUND.format(type=self.entity_type, path=self.csv_path), level="WARN")
            return []
        try:
            df = pd.read_csv(self.csv_path)
            return df.to_dict('records')
        except Exception as e:
            IPCMessenger.log(MSG_ERROR_LOADING.format(type=self.entity_type, error=e), level="ERROR")
            return []

    def _load_learned_json(self) -> dict:
        runtime_map = {}
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                for k, v in data.items():
                    if isinstance(v, str):
                        runtime_map[k] = v
                    elif isinstance(v, dict):
                        fs_id = k
                        aliases = v.get(JSON_KEY_ALIASES, [])
                        for alias in aliases:
                            runtime_map[alias] = fs_id
            except Exception:
                return {}
        return runtime_map

    def learn(self, name: str, fs_id: str):
        self.learned_mappings[name] = fs_id
        self.knowledge_base[name] = fs_id
        
        data = {}
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception:
                data = {}
        
        new_data = {}
        for k, v in data.items():
            if isinstance(v, str):
                lid, alias = v, k
                if lid not in new_data:
                    new_data[lid] = {JSON_KEY_ALIASES: []}
                if alias not in new_data[lid][JSON_KEY_ALIASES]:
                    new_data[lid][JSON_KEY_ALIASES].append(alias)
            elif isinstance(v, dict):
                if k not in new_data:
                    new_data[k] = {JSON_KEY_ALIASES: []}
                existing = set(new_data[k][JSON_KEY_ALIASES])
                for a in v.get(JSON_KEY_ALIASES, []):
                    if a not in existing:
                        new_data[k][JSON_KEY_ALIASES].append(a)
                        existing.add(a)
        
        if fs_id not in new_data:
            new_data[fs_id] = {JSON_KEY_ALIASES: []}
        
        if name not in new_data[fs_id][JSON_KEY_ALIASES]:
            new_data[fs_id][JSON_KEY_ALIASES].append(name)
            
        os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)

    def _build_search_list(self) -> List[dict]:
        raise NotImplementedError("Subclasses must implement _build_search_list")

    def _calculate_similarity(self, a: str, b: str) -> float:
        if not a or not b: return 0.0
        return SequenceMatcher(None, a.lower(), b.lower()).ratio() * 100

    def get_id_by_alias(self, alias: str) -> Optional[str]:
        if not alias:
            return None
            
        if alias in self.knowledge_base:
            return self.knowledge_base[alias]
                
        return None

    def match(self, target_name: str, interactive: bool = True) -> Optional[str]:
        if target_name in self.knowledge_base:
            return self.knowledge_base[target_name]

        best_matches = []
        for cand in self.search_candidates:
            score = self._calculate_similarity(target_name, cand['search_name'])
            if score >= config.THRESHOLD_CONFIRM_MATCH:
                best_matches.append((cand, score))
        
        best_matches.sort(key=lambda x: x[1], reverse=True)
        
        if not best_matches:
            return None

        top_cand, top_score = best_matches[0]

        if top_score >= config.THRESHOLD_AUTO_MATCH:
            self.learn(target_name, top_cand['id'])
            IPCMessenger.log(MSG_AUTO_MAPPED.format(
                original=target_name, matched=top_cand['display'], score=top_score
            ), level="INFO")
            return top_cand['id']

        if interactive:
            return self._ask_user_confirmation(target_name, best_matches[:3])
        else:
            IPCMessenger.log(MSG_BATCH_MODE_SKIP.format(original=target_name), level="WARN")
            return None

    def _ask_user_confirmation(self, target_name: str, candidates: List[Tuple[dict, float]]) -> Optional[str]:
        print(MSG_CANDIDATE_HEADER.format(original=target_name))
        for idx, (cand, score) in enumerate(candidates, 1):
            print(MSG_CANDIDATE_ITEM.format(idx=idx, name=cand['display'], score=score))
        print(MSG_SKIP_OPTION)

        while True:
            try:
                choice = input("선택 (번호 입력): ").strip()
                if not choice: continue
                
                idx = int(choice)
                if idx == 0:
                    return None
                
                if 1 <= idx <= len(candidates):
                    selected = candidates[idx-1][0]
                    self.learn(target_name, selected['id'])
                    print(MSG_SAVED_SUCCESS.format(original=target_name, matched=selected['display']))
                    return selected['id']
                else:
                    print("잘못된 번호입니다.")
            except ValueError:
                print("숫자를 입력해주세요.")
            except EOFError:
                return None

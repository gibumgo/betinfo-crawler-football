import config
from typing import Optional
from infrastructure.mapping.match_context_resolver import MatchContextResolver
from infrastructure.mapping.similarity_resolver import SimilarityResolver
from infrastructure.mapping.team_name_matcher import TeamNameMatcher
from shared.ipc_messenger import IPCMessenger

class TeamMapper:
    def __init__(self, data_dir: str = config.DIR_DATA):
        self.context_resolver = MatchContextResolver(data_dir)
        self.similarity_resolver = SimilarityResolver()
        self.name_matcher = TeamNameMatcher()
        
    def get_flashscore_id(self, betinfo_name: str, betinfo_match_date: str = None, betinfo_opponent: str = None) -> Optional[str]:
        fs_id = self.name_matcher.match(betinfo_name, interactive=False)
        if fs_id:
            return fs_id
        
        if betinfo_match_date and betinfo_opponent:
            fs_matches = self.context_resolver.find_potential_match(betinfo_match_date, betinfo_name, betinfo_opponent)
            if fs_matches:
                for match in fs_matches:
                    sim_home = self.similarity_resolver.calculate_similarity(betinfo_opponent, match['home'])
                    sim_away = self.similarity_resolver.calculate_similarity(betinfo_opponent, match['away'])
                    
                    if sim_away > 0.6:
                        self.name_matcher.learn(betinfo_name, match['home_id'])
                        IPCMessenger.log(f"🧠 Context Learned: {betinfo_name} -> {match['home_id']} (Home)", level="INFO")
                        return match['home_id']
                        
                    elif sim_home > 0.6:
                        self.name_matcher.learn(betinfo_name, match['away_id'])
                        IPCMessenger.log(f"🧠 Context Learned: {betinfo_name} -> {match['away_id']} (Away)", level="INFO")
                        return match['away_id']

        return None

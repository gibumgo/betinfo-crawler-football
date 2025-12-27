from difflib import SequenceMatcher

class SimilarityResolver:

    def __init__(self):
        pass

    def calculate_similarity(self, a: str, b: str) -> float:

        if not a or not b:
             return 0.0
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def find_best_match(self, target: str, candidates: list[dict], threshold: float = 0.6):
        best_score = 0.0
        best_candidate = None

        for cand in candidates:
            score_ko = self.calculate_similarity(target, cand.get('name_ko', ''))
            score_en = self.calculate_similarity(target, cand.get('name_en', ''))
            
            max_local = max(score_ko, score_en)
            
            if max_local > best_score:
                best_score = max_local
                best_candidate = cand

        if best_score >= threshold:
            return best_candidate, best_score
        
        return None, best_score

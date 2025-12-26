from config import DEFAULT_LEAGUE_PATH, DEFAULT_SEASON, DEFAULT_NATION, DEFAULT_LEAGUE_NAME

class InputView:
    @staticmethod
    def get_collection_params():
        print("-" * 60)
        print(f"📍 리그 경로 (예: {DEFAULT_LEAGUE_PATH})")
        league_path = input("👉 입력: ").strip() or DEFAULT_LEAGUE_PATH
        
        parts = [p for p in league_path.split('/') if p]
        if len(parts) >= 3:
            league_name = parts[2]
        else:
            league_name = "unknown_league"

        print(f"🔑 추출된 리그 이름: {league_name}")
        
        season = input(f"📅 시즌 (예: {DEFAULT_SEASON}) [엔터: {DEFAULT_SEASON}]: ").strip() or DEFAULT_SEASON
        
        print("\n[옵션] 특정 라운드 범위 수집 (엔터 입력 시 최신 라운드만)")
        start_round = input("➡️ 시작 라운드: ").strip()
        end_round = input("➡️ 종료 라운드: ").strip()
        
        return {
            "league_path": league_path,
            "league_name": league_name,
            "season": season,
            "start_round": int(start_round) if start_round.isdigit() else None,
            "end_round": int(end_round) if end_round.isdigit() else None
        }
    
    @staticmethod
    def get_metadata_params():
        print("-" * 60)
        print("📍 메타데이터 수집 정보 입력")
        print("-" * 60)
        
        nation = input(f"🌍 국가명 (예: {DEFAULT_NATION}): ").strip() or DEFAULT_NATION
        
        league_name = input(f"🏆 리그명 (예: {DEFAULT_LEAGUE_NAME}): ").strip() or DEFAULT_LEAGUE_NAME
        
        print("\n💡 리그 ID는 순위표 URL에서 확인할 수 있습니다.")
        print(f"   예: https://www.flashscore.co.kr/soccer/{DEFAULT_NATION}/{DEFAULT_LEAGUE_NAME}/standings/#/OEEq9Yvp/standings/overall/")
        print("   → 리그 ID: OEEq9Yvp")
        league_id = input("🔑 리그 ID: ").strip()
        
        if not league_id:
            print("⚠️ 리그 ID는 필수 입력값입니다.")
            return None
        
        season = input(f"📅 시즌 (예: {DEFAULT_SEASON}) [엔터: {DEFAULT_SEASON}]: ").strip() or DEFAULT_SEASON
        
        return {
            "nation": nation,
            "league_name": league_name,
            "league_id": league_id,
            "season": season
        }

class InputView:
    @staticmethod
    def get_collection_params():
        print("-" * 60)
        print("📍 리그 경로 (예: /soccer/england/premier-league/)")
        league_path = input("👉 입력: ").strip() or "/soccer/england/premier-league/"
        
        season = input("📅 시즌 (예: 2025-2026) [엔터: 2025-2026]: ").strip() or "2025-2026"
        
        print("\n[옵션] 특정 라운드 범위 수집 (엔터 입력 시 최신 라운드만)")
        start_round = input("➡️ 시작 라운드: ").strip()
        end_round = input("➡️ 종료 라운드: ").strip()
        
        return {
            "league_path": league_path,
            "season": season,
            "start_round": int(start_round) if start_round.isdigit() else None,
            "end_round": int(end_round) if end_round.isdigit() else None
        }
    
    @staticmethod
    def get_metadata_params():
        print("-" * 60)
        print("📍 메타데이터 수집 정보 입력")
        print("-" * 60)
        
        nation = input("🌍 국가명 (예: england): ").strip() or "england"
        
        league_name = input("🏆 리그명 (예: premier-league): ").strip() or "premier-league"
        
        print("\n💡 리그 ID는 순위표 URL에서 확인할 수 있습니다.")
        print("   예: https://www.flashscore.co.kr/soccer/england/premier-league/standings/#/OEEq9Yvp/standings/overall/")
        print("   → 리그 ID: OEEq9Yvp")
        league_id = input("🔑 리그 ID: ").strip()
        
        if not league_id:
            print("⚠️ 리그 ID는 필수 입력값입니다.")
            return None
        
        season = input("📅 시즌 (예: 2025-2026) [엔터: 2025-2026]: ").strip() or "2025-2026"
        
        return {
            "nation": nation,
            "league_name": league_name,
            "league_id": league_id,
            "season": season
        }

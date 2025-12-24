import os

class ConsoleView:
    @staticmethod
    def display_welcome():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 60)
        print("        🚀 FOOTBALL DATA COLLECTION SYSTEM")
        print("=" * 60)
        print("1. 벳인포 (Betinfo.co.kr) 수집")
        print("2. 플래시스코어 (Flashscore) 수집")
        print("Q. 프로그램 종료")
        print("-" * 60)

    @staticmethod
    def get_site_choice():
        choice = input("👉 원하시는 작업의 번호를 입력하세요: ").strip().upper()
        return choice

    @staticmethod
    def display_status(message: str, type: str = "info"):
        icons = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️", "working": "🔄"}
        icon = icons.get(type, "•")
        print(f"{icon} {message}")

    @staticmethod
    def display_flashscore_menu():
        print("\n" + "=" * 60)
        print("        📊 FLASHSCORE 데이터 수집")
        print("=" * 60)
        print("1. 경기 데이터 수집 (Match Data)")
        print("2. 메타데이터 수집 (League & Team Metadata)")
        print("B. 뒤로 가기")
        print("-" * 60)
    
    @staticmethod
    def get_flashscore_choice():
        choice = input("👉 원하시는 작업의 번호를 입력하세요: ").strip().upper()
        return choice

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

    @staticmethod
    def display_completion(match_count: int, filename: str):
        print("\n" + "=" * 60)
        print(f"🎉 수집 작업이 완료되었습니다!")
        print(f"📊 총 수집 경기 수: {match_count}개")
        print(f"💾 저장 파일명: {filename}")
        print("=" * 60 + "\n")

    @staticmethod
    def display_match_collection_start(season: str, league_path: str):
        print(f"\n🕒 경기 결과 수집 시작 ({season}): {league_path}")
    
    @staticmethod
    def display_match_collection_result(result: dict):
        if result['match_count'] > 0:
            print(f"💾 경기 결과 저장 완료: {result['filename']} ({result['match_count']}개)")
        else:
            print("⚠️ 수집된 경기 데이터가 없습니다. 라운드 범위나 페이지 상태를 확인하세요.")
    
    @staticmethod
    def display_loading_round(target_round: int):
        print(f"🔍 {target_round} 라운드 데이터를 찾는 중...")
    
    @staticmethod
    def display_metadata_collection_start(nation: str, league_name: str, league_id: str, season: str):
        print(f"\n{'='*60}")
        print(f"🏆 메타데이터 수집 시작")
        print(f"📍 국가: {nation}, 리그: {league_name}, ID: {league_id}")
        print(f"📅 시즌: {season}")
        print(f"{'='*60}\n")
    
    @staticmethod
    def display_metadata_collection_result(result: dict):
        if result['success']:
            print(f"\n{'='*60}")
            print("🎉 메타데이터 수집 완료!")
            print(f"📊 리그: 1개")
            print(f"📊 팀: {result['team_count']}개")
            print(f"📊 리그-팀 관계: {result['relation_count']}개")
            print(f"{'='*60}\n")
        else:
            print(f"❌ {result.get('error', '알 수 없는 오류')}")

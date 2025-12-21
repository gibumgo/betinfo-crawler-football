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
    def get_collection_params():
        print("-" * 60)
        league_path = input("📍 리그 경로 (예: /football/england/premier-league/): ").strip()
        season = input("📅 시즌 (예: 2024-2025): ").strip() or "2024-2025"
        
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
    def display_completion(match_count: int, filename: str):
        print("\n" + "=" * 60)
        print(f"🎉 수집 작업이 완료되었습니다!")
        print(f"📊 총 수집 경기 수: {match_count}개")
        print(f"💾 저장 파일명: {filename}")
        print("=" * 60 + "\n")

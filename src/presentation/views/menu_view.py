import os

class MenuView:
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
    def display_betinfo_settings():
        print("\n[Betinfo 수집 설정]")

class BetinfoMessageView:
    @staticmethod
    def display_invalid_round_input():
        print("❌ 회차는 숫자만 입력 가능합니다.")
    
    @staticmethod
    def display_processing_round(round_val: str):
        print(f"🔄 {round_val} 회차 처리 중...")
    
    @staticmethod
    def display_all_complete():
        print("✅ 모든 회차 수집이 완료되었습니다.")
    
    @staticmethod
    def display_collection_error(error):
        print(f"❌ Betinfo 수집 중 오류: {error}")

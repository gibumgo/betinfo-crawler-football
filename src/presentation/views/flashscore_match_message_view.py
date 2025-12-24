class FlashscoreMatchMessageView:
    @staticmethod
    def display_collection_start(season: str, league_path: str):
        print(f"\n🕒 경기 결과 수집 시작 ({season}): {league_path}")
    
    @staticmethod
    def display_collection_result(result: dict):
        if result['match_count'] > 0:
            print(f"💾 경기 결과 저장 완료: {result['filename']} ({result['match_count']}개)")
        else:
            print("⚠️ 수집된 경기 데이터가 없습니다. 라운드 범위나 페이지 상태를 확인하세요.")
    
    @staticmethod
    def display_loading_round(target_round: int):
        print(f"🔍 {target_round} 라운드 데이터를 찾는 중...")
    
    @staticmethod
    def display_data_complete():
        print("✅ 데이터 저장 및 후처리가 완료되었습니다.")
    
    @staticmethod
    def display_collection_error(error):
        print(f"❌ 수집 작업 중 오류 발생: {error}")

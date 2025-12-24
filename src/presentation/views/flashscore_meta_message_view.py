class FlashscoreMetaMessageView:
    @staticmethod
    def display_collection_start(nation: str, league_name: str, league_id: str, season: str):
        print(f"\n{'='*60}")
        print(f"🏆 메타데이터 수집 시작")
        print(f"📍 국가: {nation}, 리그: {league_name}, ID: {league_id}")
        print(f"📅 시즌: {season}")
        print(f"{'='*60}\n")
    
    @staticmethod
    def display_collection_result(result: dict):
        if result['success']:
            print(f"\n{'='*60}")
            print("🎉 메타데이터 수집 완료!")
            print(f"📊 리그: 1개")
            print(f"📊 팀: {result['team_count']}개")
            print(f"📊 리그-팀 관계: {result['relation_count']}개")
            print(f"{'='*60}\n")
        else:
            print(f"❌ {result.get('error', '알 수 없는 오류')}")
    
    @staticmethod
    def display_collection_canceled():
        print("⚠️ 메타데이터 수집이 취소되었습니다.")
    
    @staticmethod
    def display_navigating_to_standings():
        print("🔗 순위표 페이지로 이동 중...")
    
    @staticmethod
    def display_standings_loaded():
        print("✅ 순위표 페이지 로딩 완료")
    
    @staticmethod
    def display_parsing():
        print("🔍 메타데이터 파싱 중...")
    
    @staticmethod
    def display_saving():
        print("💾 데이터 저장 중...")
    
    @staticmethod
    def display_collection_error(error):
        print(f"❌ 메타데이터 수집 중 오류 발생: {error}")

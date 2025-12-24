import traceback
from domain.exceptions import CrawlerException, FlashscoreException, BetinfoException

class ErrorHandler:
    def __init__(self, view):
        self.view = view

    def execute(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
            
        except FlashscoreException as e:
            self.view.display_status(f"⚠️ 플래시스코어 처리 중 오류 발생: {str(e)}", "error")
            
        except BetinfoException as e:
            self.view.display_status(f"⚠️ 벳인포 처리 중 오류 발생: {str(e)}", "error")
            
        except CrawlerException as e:
            self.view.display_status(f"⚠️ 크롤러 오류: {str(e)}", "error")
            
        except Exception as e:
            self.view.display_status(f"❌ 예상치 못한 시스템 오류 발생: {str(e)}", "error")
            print("\n🔍 상세 에러 로그:")
            traceback.print_exc()
        
        finally:
            pass

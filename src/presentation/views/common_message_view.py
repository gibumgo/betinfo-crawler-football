class CommonMessageView:
    @staticmethod
    def display_browser_initializing():
        print("🔄 브라우저를 초기화 중입니다...")
    
    @staticmethod
    def display_browser_closed():
        print("ℹ️ 브라우저 세션이 종료되었습니다.")
    
    @staticmethod
    def display_invalid_choice():
        print("⚠️ 잘못된 입력입니다. 다시 선택해주세요.")
    
    @staticmethod
    def display_status(message: str, type: str = "info"):
        icons = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️", "working": "🔄"}
        icon = icons.get(type, "•")
        print(f"{icon} {message}")

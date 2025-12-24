import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from presentation.controllers.betinfo_controller import BetinfoController
from presentation.controllers.flashscore_controller import FlashscoreController
from presentation.views.console_view import ConsoleView
from infrastructure.repositories.betinfo_repository import BetinfoRepository
from infrastructure.repositories.flashscore_repository import FlashscoreRepository
from shared.error_handler import ErrorHandler
import time

def main():
    view = ConsoleView()
    error_handler = ErrorHandler(view)
    
    betinfo_repo = BetinfoRepository()
    flashscore_repo = FlashscoreRepository()
    
    betinfo_controller = BetinfoController(view, betinfo_repo, error_handler)
    flashscore_controller = FlashscoreController(view, flashscore_repo, error_handler)
    
    SITE_CONTROLLERS = {
        '1': betinfo_controller,
        '2': flashscore_controller
    }

    while True:
        view.display_welcome()
        choice = view.get_site_choice()

        if choice == 'Q':
            view.display_status("프로그램을 종료합니다. 감사합니다!", "info")
            break

        controller = SITE_CONTROLLERS.get(choice)
        
        if controller:
            controller.start_collection()
            input("\n메뉴로 돌아가려면 엔터를 누르세요...")
        else:
            view.display_status("잘못된 입력입니다. 다시 선택해주세요.", "warning")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n사용자에 의해 프로그램이 종료되었습니다.")

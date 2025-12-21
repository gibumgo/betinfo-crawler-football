from controller.betinfo_controller import BetinfoController
from controller.flashscore_controller import FlashscoreController
from view.console_view import ConsoleView
import time

def main():
    view = ConsoleView()
    
    SITE_CONTROLLERS = {
        '1': BetinfoController,
        '2': FlashscoreController
    }

    while True:
        view.display_welcome()
        choice = view.get_site_choice()

        if choice == 'Q':
            view.display_status("프로그램을 종료합니다. 감사합니다!", "info")
            break

        controller_class = SITE_CONTROLLERS.get(choice)
        
        if controller_class:
            controller = controller_class()
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

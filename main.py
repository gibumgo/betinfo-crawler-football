import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from presentation.cli.main_parser import MainParser
from presentation.controllers.betinfo_controller import BetinfoController
from presentation.controllers.flashscore_controller import FlashscoreController
from presentation.controllers.cli_betinfo_controller import CliBetinfoController
from presentation.controllers.cli_flashscore_controller import CliFlashscoreController

from presentation.views.console_view import ConsoleView
from infrastructure.repositories.betinfo_repository import BetinfoRepository
from infrastructure.repositories.flashscore_repository import FlashscoreRepository
from shared.error_handler import ErrorHandler
from shared.ipc_messenger import IPCMessenger
import time

def run_interactive_mode():
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

def run_cli_mode(args):
    try:
        if args.mode == "betinfo":
            repo = BetinfoRepository()
            controller = CliBetinfoController(repo)
            controller.run(args)
            
        elif args.mode == "flashscore":
            repo = FlashscoreRepository()
            controller = CliFlashscoreController(repo)
            controller.run(args)
            
        else:
            IPCMessenger.send_error(1, f"Unknown mode: {args.mode}")
            sys.exit(1)
            
    except Exception as e:
        IPCMessenger.send_error(99, f"Unexpected Error: {e}")
        sys.exit(99)

def main():
    parser = MainParser()
    args = parser.parse_args()
    
    if args.interactive or not args.mode:
        run_interactive_mode()
    else:
        run_cli_mode(args)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if len(sys.argv) > 1: 
             IPCMessenger.send_error(3, "Process Interrupted by User")
        else:
             print("\n\n사용자에 의해 프로그램이 종료되었습니다.")
        sys.exit(0)

from view.menu_view import MenuView
from view.input_view import InputView
from view.flashscore_match_message_view import FlashscoreMatchMessageView
from view.flashscore_meta_message_view import FlashscoreMetaMessageView
from view.betinfo_message_view import BetinfoMessageView
from view.common_message_view import CommonMessageView

class ConsoleView:
    def __init__(self):
        self.menu = MenuView()
        self.input = InputView()
        self.flashscore_match_msg = FlashscoreMatchMessageView()
        self.flashscore_meta_msg = FlashscoreMetaMessageView()
        self.betinfo_msg = BetinfoMessageView()
        self.common_msg = CommonMessageView()
    
    def display_welcome(self):
        self.menu.display_welcome()
    
    def get_site_choice(self):
        return self.menu.get_site_choice()
    
    def display_flashscore_menu(self):
        self.menu.display_flashscore_menu()
    
    def get_flashscore_choice(self):
        return self.menu.get_flashscore_choice()
    
    def display_betinfo_settings(self):
        self.menu.display_betinfo_settings()
    
    def get_collection_params(self):
        return self.input.get_collection_params()
    
    def get_metadata_params(self):
        return self.input.get_metadata_params()
    
    def display_match_collection_start(self, season: str, league_path: str):
        self.flashscore_match_msg.display_collection_start(season, league_path)
    
    def display_match_collection_result(self, result: dict):
        self.flashscore_match_msg.display_collection_result(result)
    
    def display_loading_round(self, target_round: int):
        self.flashscore_match_msg.display_loading_round(target_round)
    
    def display_match_data_complete(self):
        self.flashscore_match_msg.display_data_complete()
    
    def display_match_collection_error(self, error):
        self.flashscore_match_msg.display_collection_error(error)
    
    def display_metadata_collection_start(self, nation: str, league_name: str, league_id: str, season: str):
        self.flashscore_meta_msg.display_collection_start(nation, league_name, league_id, season)
    
    def display_metadata_collection_result(self, result: dict):
        self.flashscore_meta_msg.display_collection_result(result)
    
    def display_metadata_collection_canceled(self):
        self.flashscore_meta_msg.display_collection_canceled()
    
    def display_navigating_to_standings(self):
        self.flashscore_meta_msg.display_navigating_to_standings()
    
    def display_standings_loaded(self):
        self.flashscore_meta_msg.display_standings_loaded()
    
    def display_parsing_metadata(self):
        self.flashscore_meta_msg.display_parsing()
    
    def display_saving_data(self):
        self.flashscore_meta_msg.display_saving()
    
    def display_metadata_collection_error(self, error):
        self.flashscore_meta_msg.display_collection_error(error)
    
    def display_invalid_round_input(self):
        self.betinfo_msg.display_invalid_round_input()
    
    def display_processing_round(self, round_val: str):
        self.betinfo_msg.display_processing_round(round_val)
    
    def display_all_rounds_complete(self):
        self.betinfo_msg.display_all_complete()
    
    def display_betinfo_collection_error(self, error):
        self.betinfo_msg.display_collection_error(error)
    
    def display_browser_initializing(self):
        self.common_msg.display_browser_initializing()
    
    def display_browser_closed(self):
        self.common_msg.display_browser_closed()
    
    def display_invalid_choice(self):
        self.common_msg.display_invalid_choice()
    
    def display_status(self, message: str, type: str = "info"):
        self.common_msg.display_status(message, type)

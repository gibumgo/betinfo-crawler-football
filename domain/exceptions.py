class CrawlerException(Exception):
    def __init__(self, message: str, original_exception: Exception = None, context: dict = None):
        super().__init__(message)
        self.original_exception = original_exception
        self.context = context or {}
        
    def __str__(self):
        base_msg = super().__str__()
        if self.original_exception:
            base_msg += f" (Caused by: {type(self.original_exception).__name__}: {self.original_exception})"
        if self.context:
            base_msg += f" | Context: {self.context}"
        return base_msg

class FlashscoreException(CrawlerException):
    pass

class BetinfoException(CrawlerException):
    pass

class ScrapingException(CrawlerException):
    pass

class ParsingException(CrawlerException):
    pass

class ValidationException(CrawlerException):
    pass

class ConfigurationException(CrawlerException):
    pass

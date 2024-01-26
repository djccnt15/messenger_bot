class BotInitException(Exception):
    def __init__(self, message="init error") -> None:
        super().__init__(message)

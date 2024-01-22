class MessengerException(Exception):
    def __init__(
        self,
        api_interface: list,
        message="list of invalid API interface name: %s",
    ) -> None:
        self.api_interface = api_interface
        self.message = message % api_interface
        super().__init__(self.message)


class InvalidMessengerError(Exception):
    ...

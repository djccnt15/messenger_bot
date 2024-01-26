class EmptyUserList(Exception):
    def __init__(self, message="User list in DB is empty") -> None:
        super().__init__(message)

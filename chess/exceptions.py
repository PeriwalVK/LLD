class Invalid_Square_Name_Exception(Exception):
    def __init__(self, message):
        super().__init__(message)


class Invalid_Square_Position_Exception(Exception):
    def __init__(self, message):
        super().__init__(message)
class FatalError(Exception):


    def __init__(self, message='Encountered a Fatal error - process terminated.'):
        self.message = message
        super().__init__(message)


class UserError(FatalError):
    

    def __init__(self, message='Encountered a Fatal error caused by user - process terminated.'):
        self.message = message
        FatalError.__init__(self, message)


class ServerError(FatalError):


    def __init__(self, message='Encountered a Fatal error caused by system and/or server - process terminated.'):
        self.message = message
        FatalError.__init__(self, message)



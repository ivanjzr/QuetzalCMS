#Custom Errors for QuetzalCMSApi
# -- Custom Exceptions --
#HOw to: Custom Python Exceptions with Error Codes and Error Messages
#---------------http://stackoverflow.com/a/6180231/1747721

class CustomError(Exception):
    def __init__(self, value=''):
        self.value = value
    def __str__(self):
        return repr(self.value)


class NotFoundError(Exception):
    def __init__(self, value=''):
        self.value = value
    def __str__(self):
        return repr(self.value)


class PasswordIncorrectError(Exception):
    def __init__(self, value=''):
        self.value = value
    def __str__(self):
        return repr(self.value)



class TokenExpiredError(Exception):
    def __init__(self, value=''):
        self.value = value
    def __str__(self):
        return repr(self.value)








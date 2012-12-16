class helper:

    #Static methods do not receive "self"
    @staticmethod
    def isValidString(s=None):
        if isinstance(s, str) and s and not s==None:
            return s
        return False
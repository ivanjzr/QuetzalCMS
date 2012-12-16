

class QuetzalFactory:
    """ A python singleton """

    class __impl:




        def __init__(self):
            #Initialize factory values
            pass



        #get factory data 1
        def getData1(self):
            try:
                pass
            except Exception as e:
                return str(e)


    __instance = None
    def __init__(self):
        # Check whether we already have an instance
        if QuetzalFactory.__instance is None:
            # Create and remember instance
            QuetzalFactory.__instance = QuetzalFactory.__impl()
            # Store instance reference as the only member in the handle
        self.__dict__['_QuetzalFactory__instance'] = QuetzalFactory.__instance

    def __getattr__(self, attr):
        """ Delegate access to implementation """
        return getattr(self.__instance, attr)

    def __setattr__(self, attr, value):
        """ Delegate access to implementation """
        return setattr(self.__instance, attr, value)
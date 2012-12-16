import os, sys, platform

#Append workspace to Python Path
workspace_dir = os.path.dirname(os.path.abspath(__file__))
if workspace_dir not in sys.path:
    sys.path.append(workspace_dir)

#Load quetzal app along with configuration
from quetzal import QuetzalApplication
application = QuetzalApplication().run().wsgifunc()

#http://code.google.com/p/modwsgi/wiki/DebuggingTechniques#Error_Catching_Middleware
#from paste.exceptions.errormiddleware import ErrorMiddleware
#application = ErrorMiddleware(QuetzalApplication().run(), debug=True)


import web


err_notfound_msg = "404 Not Found"
err_internalerror_msg = "500 Internal Server Error"

#------------------custom errors-------------------------
#http://webpy.org/cookbook/custom_notfound
def notfound(msg=None):
    if msg==None:
        return web.notfound(err_notfound_msg)
    return web.notfound(msg)
    # You can use template result like below, either is ok:
    #return web.notfound(render.notfound())
    #return web.notfound(str(render.notfound()))

def internalerror(msg=None):
    if msg==None:
        return web.internalerror(err_internalerror_msg)
    return web.internalerror(msg)
#app.internalerror = internalerror
#app.notfound = notfound
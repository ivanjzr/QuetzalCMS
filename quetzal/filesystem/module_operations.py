

def load_resource_module(path, fromlist='*'):
    try:
        m = __import__(path, fromlist=fromlist)
        return m
    except Exception as e:
        raise EnvironmentError(e)
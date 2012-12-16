import quetzal.lib.introspector as intros

def load_caller(skip=4):
    return intros.caller_name(skip=skip)

def caller():
    #introspection level set to 4, who calls my call...
    _caller = load_caller(skip=4)
    parts = _caller.split('.')
    return parts[0]


def get_caller(skip=4):
    #introspection level set to 4, who calls my call...
    _caller = get_caller_name(skip=skip)
    parts = _caller.split('.')
    return parts[0]
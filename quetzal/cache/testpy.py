


import memcache
mc = memcache.Client(["127.0.0.1:11211"])
mc.set("foo","bar")
foo = mc.get("foo")


print foo
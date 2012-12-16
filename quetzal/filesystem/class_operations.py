

def iterate_resource_class(resource_module, class_prefix):
    resource_class = []
    class_name = []
    try:
        #module_items = resource_module.__dict__.items()
        for handler_name, inst in resource_module.__dict__.items():
            if handler_name.startswith(class_prefix):
                mapped_class = getattr(resource_module, handler_name)
                #Pass values
                resource_class.append(mapped_class)
                class_name.append(handler_name)
        return resource_class, class_name
    except Exception as e:
        raise TypeError(e)
import os
from quetzal import conf

quetzal_config = conf.QuetzalConfig.load()
QUETZAL_DIR = quetzal_config['quetzal_dir']


def iterate_directory(resource_name, basedir=QUETZAL_DIR):
    try:
        res_name = resource_name
        dirs = os.listdir(basedir+res_name)
        ret_list = []
        for file in dirs:
            if not (file.endswith('.pyc') or file.startswith('__') or file.endswith('.py') or file=='templates'):
                ret_list.append(file)
        return ret_list
    except Exception as e:
        raise TypeError(e)

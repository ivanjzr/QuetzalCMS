from quetzal.core.monitors import win_mon, lin_mon
import platform

def reload(quetzal_dir):
    if platform.system() == 'Windows':
        win_mon._restart(quetzal_dir)
    elif platform.system() == 'Linux':
        lin_mon.start(interval=1.0)
        lin_mon.track(quetzal_dir)
from otp.ai.AIBase import *
__builtins__['simbase'] = AIBase()
__builtins__['ostream'] = Notify.out()
__builtins__['run'] = simbase.run
__builtins__['taskMgr'] = simbase.taskMgr
__builtins__['jobMgr'] = simbase.jobMgr
__builtins__['eventMgr'] = simbase.eventMgr
__builtins__['messenger'] = simbase.messenger
__builtins__['bboard'] = simbase.bboard
__builtins__['config'] = simbase.config
__builtins__['directNotify'] = directNotify
from direct.showbase import Loader
simbase.loader = Loader.Loader(simbase)
__builtins__['loader'] = simbase.loader
directNotify.setDconfigLevels()

def inspect(anObject):
    from direct.tkpanels import Inspector
    Inspector.inspect(anObject)


__builtins__['inspect'] = inspect
if not __debug__ and __dev__:
    notify = directNotify.newCategory('ShowBaseGlobal')
    notify.error("You must set 'want-dev' to false in non-debug mode.")
taskMgr.finalInit()

# The VirtualFileSystem, which has already initialized, doesn't see the mount
# directives in the config(s) yet. We have to force it to load those manually:
from panda3d.core import VirtualFileSystem, ConfigVariableList, Filename
vfs = VirtualFileSystem.getGlobalPtr()
mounts = ConfigVariableList('vfs-mount')
for mount in mounts:
    mountfile, mountpoint = (mount.split(' ', 2) + [None, None, None])[:2]
    vfs.mount(Filename(mountfile), Filename(mountpoint), 0)

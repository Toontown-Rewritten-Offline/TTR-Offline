
def stubFunction(*args):
    pass

class LockBase:
    stateNames = ['off',
     'locking',
     'locked',
     'unlocking',
     'unlocked']
    stateDurations = [None,
     3.0,
     None,
     3.5,
     None]

class DistributedDoorEntityBase:
    stateNames = ['off',
     'opening',
     'open',
     'closing',
     'closed']
    stateDurations = [None,
     3.7,
     1.5,
     3.7,
     None]
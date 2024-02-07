from toontown.hood import GenericAnimatedProp

class GenericAnimatedBuilding(GenericAnimatedProp.GenericAnimatedProp):

    def __init__(self, node):
        GenericAnimatedProp.GenericAnimatedProp.__init__(self, node)

    def enter(self):
        if config.ConfigVariableBool('buildings-animate', False).getValue():
            GenericAnimatedProp.GenericAnimatedProp.enter(self)

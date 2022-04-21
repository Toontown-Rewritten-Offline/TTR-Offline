class DNAElement:
    TAG = '*'
    PARENTS = []

    def __init__(self):
        self.parent_ = None
        self.children = []

    def reparentTo(self, parent):
        if self.parent_:
            self.parent_.children.remove(self)

        self.parent_ = parent

        if parent:
            self.parent_.children.append(self)

    def handleText(self, chars):
        pass

    def findChildren(self, type):
        return [child for child in self.children if isinstance(child, type)]

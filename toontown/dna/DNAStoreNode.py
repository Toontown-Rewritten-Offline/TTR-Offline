from .DNAStorageElement import DNAStorageElement
from .DNAParser import *

class DNAStoreNode(DNAStorageElement):
    TAG = 'store_node'
    PARENTS = ['model']

    def __init__(self, root, code, node=None):
        DNAStorageElement.__init__(self)

        self.root = root
        self.code = code
        if node is None:
            self.node = code
        else:
            self.node = node

    def _store(self, storage):
        model = self.parent_.getModel()

        if self.node == "":
            node = model
        else:
            node = model.find('**/' + self.node)

        storage.storeNode(node, self.code, self.getScope())
        storage.storeCatalogCode(self.root, self.code)

registerElement(DNAStoreNode)

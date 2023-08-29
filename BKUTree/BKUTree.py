from typing import TypeVar, Generic, List
from queue import Queue

K = TypeVar('K')
V = TypeVar('V')
class Entry(Generic[K, V]):
    def __init__(self, key: K, value: V):
        self.key = key
        self.val = value

class AVLTree(Generic[K, V]):
    def __init__(self):
        self.root: AVLTree.Node = None
    
    class Node:
        def __init__(self, entry: Entry):
            self.entry = entry
            self.left: AVLTree.Node = None
            self.right: AVLTree.Node = None
            self.balance = 0
            self.coor: SplayTree.Node = None
    
    def __getHeight(self, root: Node) -> int:
        if root is None:
            return 0
        return 1 + max(self.__getHeight(root.left), self.__getHeight(root.right))
    
    def __getBalanceFactor(self, x: Node) -> int:
        if x is None:
            return 0
        return self.__getHeight(x.left) - self.__getHeight(x.right)
    
    def rightRotate(self, x: Node) -> Node:
        y: AVLTree.Node = x.left
        x.left = y.right
        y.right = x
        y.balance, x.balance = self.__getBalanceFactor(y), self.__getBalanceFactor(x)
        return y
    
    def leftRotate(self, x: Node) -> Node:
        y: AVLTree.Node = x.right
        x.right = y.left
        y.left = x
        y.balance, x.balance = self.__getBalanceFactor(y), self.__getBalanceFactor(x)
        return y
    
    def __LRRotate(self, x: Node) -> Node:
        x.left = self.leftRotate(x.left)
        return self.rightRotate(x)
    
    def __RLRotate(self, x: Node) -> Node:
        x.right = self.rightRotate(x.right)
        return self.leftRotate(x)
    
    def __balance(self, root: Node) -> Node:
        if root is None:
            return None
        root.balance = self.__getBalanceFactor(root)
        if root.balance > 1:
            if self.__getBalanceFactor(root.left) > 0:
                root = self.rightRotate(root)
            else:
                root = self.__LRRotate(root)
        
        elif root.balance < -1:
            if self.__getBalanceFactor(root.right) > 0:
                root = self.__RLRotate(root)
            else:
                root = self.leftRotate(root)
        
        return root
    
    def __addAVLHelper(self, root: Node, node: Node) -> Node:
        if root is None:
            root = node
        else:
            if node.entry.key < root.entry.key:
                root.left = self.__addAVLHelper(root.left, node)
            elif node.entry.key > root.entry.key:
                root.right = self.__addAVLHelper(root.right, node)
            else:
                raise RuntimeError("Duplicate Key")
            root = self.__balance(root)
        return root
    
    def __deleteAVLHelper(self, root: Node, key: K) -> Node:
        if root is None:
            raise RuntimeError("Key not found")
        
        if key < root.entry.key:
            root.left = self.__deleteAVLHelper(root.left, key)
        
        elif key > root.entry.key:
            root.right = self.__deleteAVLHelper(root.right, key)

        else:
            if root.left is None:
                temp: AVLTree.Node = root.right
                del root
                return temp
            
            elif root.right is None:
                temp: AVLTree.Node = root.left
                del root
                return temp
            
            else:
                temp: AVLTree.Node = root.left
                while temp.right is not None:
                    temp = temp.right

                root.entry = temp.entry
                root.left = self.__deleteAVLHelper(root.left, temp.entry.key)
        return self.__balance(root)
    
    def searchHelper(self, root: Node, key: K) -> Node:
        if root is None:
            return None
        
        if key < root.entry.key:
            return self.searchHelper(root.left, key)
        
        elif key > root.entry.key:
            return self.searchHelper(root.right, key)
        
        else:
            return root
    
    def __NLRHelper(self, root: Node, func) -> None:
        if root is None:
            return
        func(root.entry.key, root.entry.val)
        self.__NLRHelper(root.left, func)
        self.__NLRHelper(root.right, func)
    
    def addKeyValue(self, key: K, value: V) -> None:
        entry: Entry[K, V] = Entry[K, V](key, value)
        node: AVLTree.Node = AVLTree.Node(entry)
        self.root = self.__addAVLHelper(self.root, node)
    
    def addEntry(self, entry: Entry) -> None:
        node: AVLTree.Node = AVLTree.Node(entry)
        self.root = self.__addAVLHelper(self.root, node)
    
    def addNode(self, node: Node) -> None:
        self.root = self.__addAVLHelper(self.root, node)
    
    def remove(self, key: K):
        self.root = self.__deleteAVLHelper(self.root, key)
    
    def searchNode(self, key: K) -> Node:
        return self.__searchHelper(self.root, key)
    
    def search(self, key: K) -> V:
        found = self.searchNode(key)
        return found.entry.val

    def NLRTraversal(self, func) -> None:
        self.__NLRHelper(self.root, func)
            

            

class SplayTree (Generic[K, V]):
    def __init__(self):
        self.root: SplayTree.Node = None
    
    class Node:
        def __init__(self, entry: Entry):
            self.entry = entry
            self.left: SplayTree.Node = None
            self.right: SplayTree.Node = None
            self.parent: SplayTree.Node = None
            self.coor: AVLTree.Node = None

    def leftRotate(self, x: Node) -> Node:
        y: SplayTree.Node = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rightRotate(self, x: Node) -> Node:
        y: SplayTree.Node = x.left
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y
    
    def splay(self, x: Node) -> None:
        while x.parent is not None:
            if x.parent.parent is None:
                if x == x.parent.left:
                    self.rightRotate(x.parent)
                else:
                    self.leftRotate(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                self.rightRotate(x.parent.parent)
                self.rightRotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                self.leftRotate(x.parent.parent)
                self.leftRotate(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.right:
                self.rightRotate(x.parent)
                self.leftRotate(x.parent)
            else:
                self.leftRotate(x.parent)
                self.rightRotate(x.parent)
    
    def one_splay(self, x: Node) -> None:
        if x.parent is not None:
            if x.parent.parent is None:
                if x == x.parent.left:
                    self.rightRotate(x.parent)
                else:
                    self.leftRotate(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                self.rightRotate(x.parent.parent)
                self.rightRotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                self.leftRotate(x.parent.parent)
                self.leftRotate(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.right:
                self.rightRotate(x.parent)
                self.leftRotate(x.parent)
            else:
                self.leftRotate(x.parent)
                self.rightRotate(x.parent)

    def __addSplayHelper(self, node: Node) -> None:
        x, y = self.root, None
        while x is not None:
            y = x
            if x.entry.key < node.entry.key:
                x = x.right
            elif x.entry.key > node.entry.key:
                x = x.left
            else:
                raise RuntimeError("Duplicate Key")
        node.parent = y
        if y is None:
            self.root = node
            return
        elif node.entry.key < y.entry.key:
            y.left = node
        else:
            y.right = node

        self.splay(node)
            

    def __searchHelper(self, root: Node, key: K) -> Node:
        if root is None:
            return None
        
        if key < root.entry.key:
            return self.__searchHelper(root.left, key)
        
        elif key > root.entry.key:
            return self.__searchHelper(root.right, key)
        
        else:
            return root
    
    def __findMax(self, x: Node) -> Node:
        while x.right is not None:
            x = x.right
        return x
    
    def __join(self, s: Node, t: Node) -> Node:
        if s is None:
            return t
        x: SplayTree.Node = self.__findMax(s)
        self.splay(x)
        x.right = t
        if t is not None:
            t.parent = x
        return x
    
    def __deleteSplayHelper(self, root: Node, key: K) -> None:
        x: SplayTree.Node = None
        temp: SplayTree.Node = root
        while temp is not None:
            if temp.entry.key == key:
                x = temp
                break
            if temp.entry.key < key:
                temp = temp.right
            else:
                temp = temp.left

        if x is None:
            raise RuntimeError("Key not found")
        
        self.splay(x)
        s, t = None, None
        if x.right is not None:
            t = x.right
            t.parent = None
        else:
            t = None
        s = x
        s.right = None
        x = None

        self.root = self.__join(s.left, t)
        s = None
    
    def __NLRHelper(self, root: Node, func) -> None:
        if root is None:
            return
        func(root.entry.key, root.entry.val)
        self.__NLRHelper(root.left, func)
        self.__NLRHelper(root.right, func)

    def addKeyValue(self, key: K, value: V) -> None:
        entry: Entry[K, V] = Entry[K, V](key, value)
        node: AVLTree.Node = AVLTree.Node(entry)
        self.__addSplayHelper(node)
    
    def addEntry(self, entry: Entry) -> None:
        node: AVLTree.Node = AVLTree.Node(entry)
        self.__addSplayHelper(node)
    
    def addNode(self, node: Node) -> None:
        self.__addSplayHelper(node)
    
    def remove(self, key: K):
        self.__deleteSplayHelper(self.root, key)
    
    def searchNode(self, key: K) -> Node:
        return self.__searchHelper(self.root, key)
    
    def search(self, key: K) -> V:
        found = self.searchNode(key)
        self.splay(found)
        return found.entry.val

    def NLRTraversal(self, func) -> None:
        self.__NLRHelper(self.root, func)

class BKUTree(Generic[K, V]):
    def __init__(self, maxNumKey: int = 5):
        self.avl: AVLTree[K, V] = AVLTree[K, V]()
        self.splay: SplayTree[K, V] = SplayTree[K, V]()
        self.keys: Queue[K] = Queue(maxsize = maxNumKey)
        self.maxNumKey = maxNumKey
    
    def add(self, key: K, val: V) -> None:
        entry: Entry = Entry(key, val)
        avlNode: AVLTree.Node = AVLTree.Node(entry)
        splayNode: SplayTree.Node = SplayTree.Node(entry)
        avlNode.coor = splayNode
        splayNode.coor = avlNode
        self.avl.addNode(avlNode)
        self.splay.addNode(splayNode)
        if self.keys.full():
            self.keys.get_nowait()
        else:
            self.keys.put_nowait(key)
    
    def remove(self, key: K) -> None:
        self.avl.remove(key)
        self.splay.remove(key)
        keys: List[K] = []
        while not self.keys.empty():
            k = self.keys.get_nowait()
            if k != key:
                keys.append(k)
        
        while len(keys) > 0:
            self.keys.put_nowait(keys[0])
            keys = keys[1:]
        
        self.keys.put_nowait(self.splay.root.entry.key)
    
    def traverseNLROnAVL(self, func) -> None:
        self.avl.NLRTraversal(func)

    def traverseNLROnSplay(self, func) -> None:
        self.splay.NLRTraversal(func)
    
    def search(self, key: K) -> V:
        if self.splay.root.entry.key == key:
            if self.keys.full():
                self.keys.get_nowait()
            else:
                self.keys.put_nowait(key)
            return self.splay.root.entry.val
        
        flag = False
        keys: List[K] = []
        while not self.keys.empty():
            k = self.keys.get_nowait()
            if k == key:
                flag = True
            keys.append(k)

        while len(keys) > 0:
            self.keys.put_nowait(keys[0])
            keys = keys[1:]
        
        if flag:
            found: SplayTree.Node = self.splay.searchNode(key)
            self.splay.one_splay(found)
            if self.keys.full():
                self.keys.get_nowait()
            else:
                self.keys.put_nowait(key)

            return found.entry.val
        
        ref_root_splay: AVLTree.Node = self.splay.root.coor
        found = self.avl.searchHelper(ref_root_splay, key)
        if found is not None:
            if self.keys.full():
                self.keys.get_nowait()
            else:
                self.keys.put_nowait(key)
            return found.entry.val
        else:
            ref_root_avl: AVLTree.Node = self.avl.root
            flag = False
            while ref_root_avl is not None:
                if ref_root_avl == ref_root_splay:
                    raise RuntimeError("Key not found")
                
                if ref_root_avl.entry.key == key:
                    flag = True
                    break
                
                if ref_root_avl.entry.key < key:
                    ref_root_avl = ref_root_avl.right
                
                else:
                    ref_root_avl = ref_root_avl.left
            if flag:
                ref_splay: SplayTree.Node = ref_root_avl.coor
                self.splay.one_splay(ref_splay)
                if self.keys.full():
                    self.keys.get_nowait()
                else:
                    self.keys.put_nowait(key)
                
                return ref_root_avl.entry.val

            raise RuntimeError("Key not found")










"""
UMass ECE 241 - Advanced Programming
Project #1     Fall 2018
SongLibrary.py - SongLibrary class
"""

from Song import Song
import random
import time
#class TreeNode creates nodes for BST
class TreeNode:
    def __init__(self, key, val, left=None, right=None, parent=None):
        self.key = key
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def replaceNodeData(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

#class BST creates Binary Search Tree
class BinarySearchTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def put(self, key, val):
        if self.root:
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1

    def _put(self, key, val, currentNode):
        if key < currentNode.key:
            if currentNode.hasLeftChild():
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent=currentNode)
        else:
            if currentNode.hasRightChild():
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent=currentNode)

    def __setitem__(self, k, v):
        self.put(k, v)

    def get_Node(self,key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res
            else:
                return None
        else:
            return None

    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None

    def _get(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)

    def __getitem__(self, key):
        return self.get(key)

    def __contains__(self, key):
        if self._get(key, self.root):
            return True
        else:
            return False


class SongLibrary:
    """
    Intialize your Song library here.
    You can initialize an empty songArray, empty BST and
    other attributes such as size and whether the array is sorted or not

    """

    def __init__(self):
        self.songArray = list()
        self.songBST = None
        self.isSorted = False
        self.size = 0

    """
    load your Song library from a given file. 
    It takes an inputFilename and store the songs in songArray
    """

    def loadLibrary(self, inputFilename):
        with open(inputFilename, 'r') as csvfile:
            for row in csvfile:
                newSong = Song(row)
                self.songArray.append(newSong)
        self.size = len(self.songArray)

    """
    Linear search function.
    It takes a query string and attibute name (can be 'title' or 'artist')
    and return the number of songs fonud in the library.
    Return -1 if no songs is found.
    Note that, Each song name is unique in the database,
    but each artist can have several songs.
    """

    def linearSearch(self, query, attribute):
        found = -1
        if attribute is "title":
            for i in range(0, self.size):
                if self.songArray[i].title == query:
                    found += 1
        elif attribute is "artist":
            for j in range(0, self.size):
                if self.songArray[j].artist == query:
                    found += 1
        return found+1

    """
    Build a BST from your Song library based on the song title. 
    Store the BST in songBST variable
    """

    def buildBST(self):
        if not self.isSorted:
            self.quickSort()
        bstree = BinarySearchTree()
        alist = self.songArray
        self.songBST = self.builderBST(bstree, alist)
        # print(self.heightChecker(self.songBST.root))

    #function to check the height of the tree. Uncomment the line above to display the height
    def heightChecker(self, node):
        if node is None:
            return 0
        else:
            leftDepth = self.heightChecker(node.leftChild)
            rightDepth = self.heightChecker(node.rightChild)
            if leftDepth > rightDepth :
                return leftDepth+1
            else:
                return rightDepth+1
    # recursive function to build the BST and add it to the object bstree
    def builderBST(self, bstree, alist):
        if len(alist) == 1:
            bstree.put(alist[0].title, alist[0])
        elif len(alist) == 2:
            bstree.put(alist[0].title, alist[0])
            bstree.put(alist[1].title, alist[0])
            return
        else:
            center = len(alist) // 2
            root = alist[center]
            bstree.put(root.title, root)
            leftsplit = alist[:center]
            rightsplit = alist[center+1:]

            self.builderBST(bstree, leftsplit)
            self.builderBST(bstree, rightsplit)

            return bstree

    """

        Return the song information string
        (After you find the song object, call the toString function)
        or None if no such song is found.
    """

    def searchBST(self, query):
        found = None
        currentNode = self.songBST.root
        while found is None and currentNode is not None:
            if currentNode.payload.title == query:
                return currentNode.payload.toString()
            elif currentNode.payload.title > query:
                currentNode = currentNode.leftChild
            elif currentNode.payload.title < query:
                currentNode = currentNode.rightChild
        return found

    """
    Return song libary information
    """

    def libraryInfo(self):
        return "Size: " + str(self.size) + ";  isSorted: " + str(self.isSorted)

    """
    Sort the songArray using QuickSort algorithm based on the song title.
    The sorted array should be stored in the same songArray.
    Remember to change the isSorted variable after sorted
    """

    def quickSort(self):
        self.quickSortHelper(self.songArray, 0, self.size-1)
        self.isSorted = True

    def quickSortHelper(self, songArray, first, last):
        if first < last:
            split = self.partition(songArray, first, last)
            self.quickSortHelper(songArray, first, split - 1)
            self.quickSortHelper(songArray, split + 1, last)

    def partition(self,songArray, first, last):
        pivot = songArray[first].title
        left = first + 1
        right = last
        while True:
            while songArray[right].title >= pivot and right >= left:
                right = right - 1
            while left <= right and songArray[left].title <= pivot:
                left = left + 1
            if right < left:
                break
            else:
                temp = songArray[left]
                songArray[left] = songArray[right]
                songArray[right] = temp

        temp = songArray[first]
        songArray[first] = songArray[right]
        songArray[right] = temp

        return right
# WRITE YOUR OWN TEST UNDER THAT IF YOU NEED
if __name__ == '__main__':
    songLib = SongLibrary()
    songLib.loadLibrary("TenKsongs.csv")

    # linear search in sorted database
    if not songLib.isSorted:
        songLib.quickSort()
    alist = []
    k = 0
    while k < 100:
        randvalue = random.randint(0, songLib.size)
        alist.append(songLib.songArray[randvalue].title)
        k += 1
    alist.sort()
    start = time.perf_counter()
    for i in range(0,100):
        songLib.linearSearch(alist[i],"title")
    done = time.perf_counter()
    print("Time taken for linear search", (done-start)/100)

    # time for BST building
    start = time.perf_counter()
    songLib.buildBST()
    done = time.perf_counter()
    print("Time taken to build the BST", (done-start))

    #time taken for BST searching
    start = time.perf_counter()
    for i in range(0, 100):
        songLib.searchBST(alist[i])
    done = time.perf_counter()
    print("Time taken for BST search", (done - start) / 100)
    print(songLib.libraryInfo())
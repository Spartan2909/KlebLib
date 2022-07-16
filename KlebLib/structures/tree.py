"""Tree -- a binary tree
"""
from typing import Any
from copy import deepcopy

__all__ = ['Tree']

class Tree:
    r"""A loosely-typed tree structure. 

    Methods:
    max_depth() -- the maximum depth of the tree
    min_depth() -- the minimum depth of the tree
    asdict() -- the tree in dictionary form
    values() -- the values of the tree as list

    Static Attributes:
    sampleDict -- a sample dictionary to demonstrate how to build a tree using a dictionary

    Indexing:
    elements can be accessed and changed using indices. the tree is navigated using '>' and '<' to move left or right respectively. 
    for example, the element 'llr' in Tree.sampleDict would be accessed with the index '<<>'. 
    the index can be prefixed with '\\' (or '\' in a raw string) to access the branch starting from that element.
    """
    def __new__(cls, item, l=None, r=None, *args, **kwargs):
        if type(item) is Tree:
            return item
        else:
            return super(Tree, cls).__new__(cls, *args, **kwargs)
        
    def __init__(self, item:Any, l=None, r=None):
        #print(f'creating tree from item {item}, left {l}, and right {r}') #debug
        
        if type(item) is dict and l is None and r is None:
            self.value = list(item.keys())[0]
            #print(f'self value is {self.value}') #debug
            sub = list(item.values())[0]
            if sub == {None: None}:
                sub = None
            #print(f'sub is {sub}') #debug
            
            if sub is None:
                self.l = None
                self.r = None
                
            else:
                keys = list(sub.keys())
                values = list(sub.values())
                #print(f'sub is {sub}, keys are {keys}, values are {values}') #debug
                
                self.l = Tree({
                    str(keys[0]): values[0]
                })
                #print(f'self.l is {self.l}') #debug

                self.r = Tree({
                    str(keys[1]): values[1]
                })
                #print(f'self.r is {self.r}') #debug
            
        else:
            self.value = item
            self.l = Tree(l)
            self.r = Tree(r)

    def __repr__(self):
        return f'KlebLib.structures.tree.Tree({self.asdict()})'

    def __str__(self):
        return str(self.asdict())

    def asdict(self):
        #print(f'creating dict from tree item {self.value}') #debug
        left = self.l.asdict() if self.l else {None: None}
        #print(f'left is {left}') #debug
        right = self.r.asdict() if self.r else {None: None}
        #print(f'right is {right}') #debug

        #print('returning {}'.format({self.value: {**left, **right}})) #debug
        return {self.value: {**left, **right}}

    def __iter__(self):
        for item in self.values():
            yield item

    def __getitem__(self, index):
        if index == 0:
            return self.value
            
        elif type(index) is str:
            if index[0] == '\u005c':
                branch = True
                index = index[1:]
            else:
                branch = False

            current = self
            for direction in index:
                #print(f'current is {self}') #debug
                if direction == '<':
                    current = current.l
                elif direction == '>':
                    current = current.r
                else:
                    raise ValueError(f'invalid value for Tree index {direction}')
    
                if current is None:
                    raise IndexError('tree index out of depth')

            if branch:
                return current
            else:
                return current.value

        else:
            raise KeyError(str(index))

    def __setitem__(self, index, item):
        if index == 0:
            self.value = item
            
        elif type(index) is str:
            current = self
            for direction in index:
                #print(f'current is {self}') #debug
                if direction == '<':
                    current = current.l
                elif direction == '>':
                    current = current.r
                else:
                    raise ValueError(f'invalid value for Tree index {direction}')
    
                if current is None:
                    raise IndexError('tree index out of depth')

            current.value = item

        else:
            raise KeyError(str(index))

    def copy(self):
        return Tree(self.asdict())

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo=None):
        return Tree(deepcopy(self.asdict()))

    def values(self):
        return Tree.get_values(self.asdict())

    def max_depth(self):
        if self.l is not None:
            lDepth = self.l.max_depth
        else:
            lDepth = -1

        if self.r is not None:
            rDepth = self.r.max_depth
        else:
            rDepth = -1

        if lDepth > rDepth:
            return lDepth + 1
        else:
            return rDepth + 1

    def min_depth(self):
        if self.l is not None:
            lDepth = self.l.min_depth
        else:
            lDepth = -1

        if self.r is not None:
            rDepth = self.r.min_depth
        else:
            rDepth = -1

        if lDepth < rDepth:
            return lDepth + 1
        else:
            return rDepth + 1

    @staticmethod
    def get_values(inputDict):
        values = []
        
        for item, links in inputDict.items():
            values.append(item)
            if links is not None:
                values += Tree.get_values(links)

        while None in values:
            values.remove(None)
        return values
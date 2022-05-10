"""Series -- a strictly-typed, linear data structure"""
from typing import Any
from copy import deepcopy

__all__ = ['Series']

class Series:
    """A strictly-typed, linear data structure of variable length. 

    Methods:
    insert(index, value) -- sets the given index to the given value, incrementing the index of the item already at that index, and all items after it, by 1
    copy() -- returns a copy of the series, keeping all references to mutable objects
    """
    def __init__(self, item:Any, seriesType:type=None, subType:type=None):
        """Create a series.
        
        Arguments:
        item -- the item to be turned into a series. values of iterables will be extracted, unless seriesType is specified as that iterable
        seriesType -- the type of the items within the series (defaults to the type of 'item')
        subType -- the type of the series within this series (default None)
        """
        #print(f'creating series from item {item}') #debug
        skip = False

        if type(item) is seriesType:
            #print('using given type') #debug
            self.value = item
            self.type = seriesType
            self.next = None
            skip = True
            
        elif type(item) is set or type(item) is tuple:
            #print(f'converting item from {type(item)} to list') #debug
            item = list(item)
            
        elif type(item) is not list:
            if seriesType and type(item) is not seriesType:
                raise TypeError(f'type of given item {item} is not the same as given type {seriesType}')
                
            self.value = item
            self.type = type(item)
            self.next = None
            
        if (type(item) is list) and (not skip):
            if seriesType and type(item[0]) is not seriesType:
                raise TypeError(f'type of given item {item[0]} is not the same as given type {seriesType}')
                
            for subItem in item:
                if type(subItem) is not type(item[0]):
                    raise TypeError('container passed to series must be of uniform type')
                    
            self.type = type(item[0])
            self.value = item[0]
            if len(item) > 1:
                self.next = Series(item[1:])
            else:
                self.next = None

        if subType is not None:
            if seriesType is not Series:
                raise TypeError('series type must be series if subtype is given')

            self.subType = subType
            for series in self:
                if series.type != subType:
                    raise TypeError(f'series type {series.type} must be equal to subtype {subType}')
        else:
            self.subType = None

    def __add__(self, other):
        result = deepcopy(self)

        if type(other) is self.type or Series.valid_conversion(other, self.type):
            other = self.type(other)
            if result.subType is not None and type(other) is not result.subType:
                raise TypeError(f'series of type {other.type} cannot be appended to series of subtype {self.subType}')
                
            result.objects()[-1].next = Series(other, type(other))
            return result

        elif type(other) is list or type(other) is tuple or type(other) is set:
            other = Series(other)
        
        if type(other) is Series:
            if self.type != other.type:
                raise TypeError(f'cannot add series of type {other.type} to series of type {self.type}')

            result.objects()[-1].next = other
            
        else:
            raise TypeError(f'cannot add object of type {type(other)} to series of type {self.type}')

        return result

    def __radd__(self, other):
        if type(other) is self.type:
            output = Series(other)
            output.next = self.deepcopy()
            
        elif type(other) is list or type(other) is tuple or type(other) is set:
            output = Series(other)
            if output.type != self.type:
                raise TypeError(f'cannot add series of type {self.type} to container containing type {other.type}')

            output.objects()[-1].next = self.deepcopy()
            
        else:
            raise IndexError(f'cannot add series of type {self.type} to object of type {type(other)}')

        return output

    def __iadd__(self, other):
        if type(other) is self.type or Series.valid_conversion(other, self.type):
            other = self.type(other)
            self.objects()[-1].next = Series(other, type(other))
            return self
        
        elif type(other) is list or type(other) is tuple or type(other) is set:
            other = Series(other)
            
        if type(other) is Series:
            if self.type != other.type:
                raise TypeError(f'cannot add series of type {other.type.__name__} to series of type {self.type.__name__}')

            self.objects()[-1].next = other
            
        else:
            raise TypeError(f'cannot add object of type {type(other).__name__} to series of type {self.type.__name__}')

        return self

    def __repr__(self):
        output = 'KlebLib.structures.series.Series(['
        for i, item in enumerate(self):
            output += repr(item)
            
            if i != len(self) - 1:
                output += ', '

        if self.type is Series:
            output += f'], KlebLib.structures.series.Series'
        else:
            output += f'], {self.type.__name__}'
            
        if self.subType is not None:
            if self.subType is Series:
                output += ', KlebLib.structures.series.Series'
            else:
                output += f', {self.subType.__name__}'

        output += ')'

        return output

    def __str__(self):
        #print(f'coverting series with head value {self.value} to str') #debug
        output = '<'
        for i, item in enumerate(self):
            output += str(item)
            
            if i != len(self) - 1:
                output += ', '

        output += '>'
        return output

    def __list__(self):
        return [item for item in self]

    def __tuple__(self):
        return tuple(list(self))

    def __set__(self):
        return set(list(self))

    def __len__(self):
        if self.value is not None:
            length = 1
            current = self
            while current.next is not None:
                length += 1
                current = current.next

            return length
            
        else:
            return 0

    def __iter__(self):
        self.iterIndex = -1
        return self

    def __next__(self):
        self.iterIndex += 1
        if self.iterIndex >= len(self):
            raise StopIteration
            
        return self[self.iterIndex]

    def __getitem__(self, index:int):
        if index >= len(self) or -index > len(self):
            raise IndexError('series index out of range')

        return self.objects()[index].value

    def __setitem__(self, index, value):
        if index >= len(self) or -index > len(self):
            raise IndexError('series index out of range')

        self.objects()[index].value = value

    def __delitem__(self, index):
        if index >= len(self) or -index > len(self):
            raise IndexError('series index out of range')
            
        self.objects()[index-1].next = self.objects()[index+1]

    def objects(self):
        #print(f'getting objects of series with head {self.value}') #debug
        result = [self]
        current = self
        while current.next is not None:
            #print(f'value of current object is {current.value}') #debug
            current = current.next
            result.append(current)

        #print('got objects') #debug
        return result

    def insert(self, index, value):
        temp = self.objects()[index]
        self.objects()[index-1].next = Series(value)
        self.objects()[index].next = temp
        del temp

    def copy(self):
        output = Series(self[0], self.type, self.subType)
        current = output
        for i in range(1, len(self)):
            current.next = Series(self[i], self.type, self.subType)
            current = current.next

        return output

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo=None):
        try:
            output = Series(deepcopy(self[0]), self.type, self.subType)
            
        except AttributeError:
            output = Series(self[0], self.type, self.subType)
            current = output
            for i in range(1, len(self)):
                current.next = Series(self[i])
                current = current.next
                
        else: #continue code in try block
            current = output
            for i in range(1, len(self)):
                current.next = Series(self[i].deepcopy(), self.type, self.subType)
                current = current.next

        return output

    @staticmethod
    def valid_conversion(item, ansType):
        try:
            ansType(item)
        except TypeError:
            return False
        else:
            return True
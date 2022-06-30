"""Fraction -- accurately store and manipulate fractions"""
import re
from numbers import Number

class Fraction:
    """Store a fraction as a numerator and denominator.

    Methods:
    mixed() -- returns a mixed fraction in its simplest form.

    Attributes:
    num -- the numerator of the fraction.
    dem -- the denominator of the fraction.
    nums -- a list of the numerator and denominator in the form [num, dem]
    """
    def __init__(self, fraction:int|float|str|list):
        """Create a fraction. 

        Arguments:
        fraction -- value of the fraction. valid formats: 
            a number as an int, float, or string
            a string in the form 'num/dem'
            a list in the form [num, dem]
        """
        self.skipSimplify = True
        
        if type(fraction) is list:
            self.num = fraction[0]
            self.dem = fraction[1]
            
        elif type(fraction) is str:
            if '/' in fraction:
                fractionNums = fraction.split('/')
                fractionNums = [int(i) for i in fractionNums]
                self.num = fractionNums[0]
                self.dem = fractionNums[1]
            else:
                self.nums = Fraction.num_to_fraction(fraction).nums

        elif type(fraction) is int or type(fraction) is float:
            fractionNums = Fraction.num_to_fraction(fraction)
            self.num = fractionNums[0]
            self.dem = fractionNums[1]
            
        else:
            raise TypeError(f'cannot parse type {type(fraction).__name__}')

        self.simplify()

    #Compares this fraction to another
    def __eq__(self, other):
        if type(other) is Fraction:
            return self.num == other.num and self.dem == other.dem
        elif isinstance(other, Number):
            return float(self) == other
        else:
            return NotImplemented

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return float(self) > float(other)

    def __ge__(self, other):
        return not self < other

    def __lt__(self, other):
        return float(self) < float(other)

    def __le__(self, other):
        return not self > other

    # Adds another fraction to this one and returns a new fraction
    def __add__(self, other):
        if type(other) is not Fraction:
            try:
                other = Fraction.num_to_fraction(other)
            except TypeError:
                return NotImplemented
            
        return Fraction.add(self, other)

    # Subtracts another fraction from this one and returns a new fraction
    def __sub__(self, other):
        if type(other) is not Fraction:
            try:
                other = Fraction.num_to_fraction(other)
            except TypeError:
                return NotImplemented
                
        return Fraction.sub(self, other)

    # Multiplies another fraction by this one and returns a new fraction
    def __mul__(self, other):
        if type(other) is not Fraction:
            try:
                other = Fraction.num_to_fraction(other)
            except TypeError:
                return NotImplemented
                
        return Fraction.mul(self, other)

    # Divides this fraction by another one and returns a new fraction
    def __truediv__(self, other):
        if type(other) is not Fraction:
            try:
                other = Fraction.num_to_fraction(other)
            except TypeError:
                raise TypeError(f'Cannot add type {type(other)} to fraction')
                
        return Fraction.truediv(self, other)

    # Adds another fraction to this one and returns a new fraction
    def __radd__(self, number):
        #print(f'adding self to {number}') #debug
        try:
            other = Fraction.num_to_fraction(number)
        except TypeError:
            return NotImplemented
            
        return Fraction.add(other, self)

    # Subtracts another fraction from this one and returns a new fraction
    def __rsub__(self, number):
        #print(subtracting self from {number}') #debug
        try:
            other = Fraction.num_to_fraction(number)
        except TypeError:
            return NotImplemented
            
        return Fraction.sub(other, self)

    # Multiplies another fraction by this one and returns a new fraction
    def __rmul__(self, number):
        #print(multiplying {number} by self') #debug
        try:
            other = Fraction.num_to_fraction(number)
        except TypeError:
            return NotImplemented
        
        return Fraction.mul(other, self)

    # Divides this fraction by another one and returns a new fraction
    def __rtruediv__(self, number):
        #print(dividing {number} by self') #debug
        try:
            other = Fraction.num_to_fraction(number)
        except TypeError:
            return NotImplemented
        
        return Fraction.truediv(other, self)

    # Adds this fraction to another one and replaces this fraction with the result
    def __iadd__(self, other):
        if type(other) is not Fraction:
            try:
                other = Fraction.num_to_fraction(other)
            except TypeError:
                return NotImplemented
                
        answer = Fraction.add(self, other)
        
        self.num = answer.num
        self.dem = answer.dem
        return self

    # Subtracts another fraction from this one and replaces this fraction with the result
    def __isub__(self, other):
        if type(other) is not Fraction:
            try:
                other = Fraction.num_to_fraction(other)
            except TypeError:
                return NotImplemented
                
        answer = Fraction.sub(self, other)
        
        self.num = answer.num
        self.dem = answer.dem
        return self

    # Multiplies this fraction by another one and replaces this fraction with the result
    def __imul__(self, other):
        if type(other) is not Fraction:
            try:
                other = Fraction.num_to_fraction(other)
            except TypeError:
                return NotImplemented
                
        answer = Fraction.mul(self, other)
        
        self.num = answer.num
        self.dem = answer.dem
        return self

    # Divides this fraction by another one and replaces this fraction with the result
    def __itruediv__(self, other):
        if type(other) is not Fraction:
            try:
                other = Fraction.num_to_fraction(other)
            except TypeError:
                return NotImplemented
                
        answer = Fraction.truediv(self, other)
        
        self.num = answer.num
        self.dem = answer.dem
        return self

    # Flips this fraction between positive and negative
    def __neg__(self):
        return Fraction([-self.num, self.dem])

    # Returns the reciprocal of this fraction
    def invert(self):
        return Fraction([self.dem, self.num])

    def __repr__(self):
        return f'KlebLib.maths.fraction.Fraction([{self.num}, {self.dem}])'

    # Output the fraction as an int
    def __int__(self):
        return int(self.num / self.dem)

    # Output the fraction as a float
    def __float__(self):
        return self.num / self.dem

    # Output the numbers as a fraction
    def __str__(self):
        if self.dem != 1:
            superscriptMap = {'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '-': '⁻'}
            subscriptMap = {'0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉', '-': '₋'}
            num = Fraction.translate(str(self.num), superscriptMap)
            dem = Fraction.translate(str(self.dem), subscriptMap)
            
            return num + '\u2044' + dem
        else:
            return str(self.num)

    # Returns either the numerator or denominator, as if the fraction were a list in form [num, dem]
    def __getitem__(self, index):
        match index:
            case 0:
                return self.num
            case 1:
                return self.dem
            case _:
                raise IndexError(f'Invalid value for Fraction index: {index}. Must be 0 or 1')

    def __setitem__(self, index, item):
        match index:
            case 0:
                self.num = item
            case 1:
                self.dem = item
            case _:
                raise IndexError(f'Invalid value for Fraction index: {index}. Must be 0 or 1')

    def __setattr__(self, attr, value):
        super().__setattr__(attr, value)
        
        if attr == 'num' or attr == 'dem':
            if self.skipSimplify and attr == 'dem':
                self.skipSimplify = False
            elif not self.skipSimplify:
                self.simplify()

    #Get the greatest common divisor of the numerator and denominator
    @property
    def GCD(self) -> int:
        #print(f'finding GCD of {self.num}/{self.dem}') #debug
        num1 = self.num
        num2 = self.dem

        if num1 < num2:
            temp = num1
            num1 = num2
            num2 = temp

        remainder = num1 % num2
        while remainder != 0:
            num1 = num2
            num2 = remainder

            remainder = num1 % num2

        #print(f'GCD is {abs(num2)}') #debug
        return abs(num2)

    #Simplify the fraction
    def simplify(self) -> None:
        #print(f'simplifying {self}') #debug
        self.skipSimplify = True
        
        num = self.num
        dem = self.dem

        #Ensure that negatives are represented in the numerator and there is no double negative
        if dem < 0:
            #print('flipping negatives') #debug
            num = -num
            dem = -dem

        num //= self.GCD
        dem //= self.GCD

        self.num = num
        self.dem = dem

    #Returns a mixed fraction
    def mixed(self):
        """Returns a mixed fraction in its simplest form."""
        integerPart = 0
        num = self.num
        dem = self.dem

        while num > dem:
            num -= dem
            integerPart += 1

        return f'{integerPart} {num}/{dem}'

    #Returns a list of the numerator and denominator
    @property
    def nums(self):
        return ([self.num, self.dem])

    #Updates the fraction through the use of nums
    @nums.setter
    def nums(self, numsList):
        self.num = numsList[0]
        self.dem = numsList[1]

        self.simplify()

    @staticmethod
    def translate(string:str, table:dict) -> str:
        trans = str.maketrans(
            ''.join(table.keys()),
            ''.join(table.values())
        )

        return string.translate(trans)
        
    #Adds two given fractions
    @staticmethod
    def add(fraction1, fraction2):
        num = (fraction1.num * fraction2.dem) + (fraction1.dem * fraction2.num)
        dem = fraction1.dem * fraction2.dem

        return Fraction([num, dem])

    #Subtracts two given fractions
    @staticmethod
    def sub(fraction1, fraction2):
        num = (fraction1.num * fraction2.dem) - (fraction1.dem * fraction2.num)
        dem = fraction1.dem * fraction2.dem

        return Fraction([num, dem])

    #Multiplies two given fractions
    @staticmethod
    def mul(fraction1, fraction2):
        num = fraction1.num * fraction2.num
        dem = fraction1.dem * fraction2.dem

        return Fraction([num, dem])

    #Divides two given fractions
    @staticmethod
    def truediv(fraction1, fraction2):
        num = fraction1.num * fraction2.dem
        dem = fraction1.dem * fraction2.num

        return Fraction([num, dem])

    @staticmethod
    def num_to_fraction(number):
        number = float(number)
            
        decPlaces = len(str(number)[re.search(r'\.', str(number)).start() + 1:])
        if re.search(r'\.0$', str(number)):
            decPlaces = 0
        number *= 10**decPlaces

        return Fraction([int(number), 10**decPlaces])
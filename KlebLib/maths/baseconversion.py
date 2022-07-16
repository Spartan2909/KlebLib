"""convert_base -- convert numbers between two specified bases.
detect_base -- detect the base of a given number
"""
from math import log
from pathlib import Path

__all__ = ['convert_base', 'detect_base']

p = Path('KlebLib/maths/chars.txt')
with p.open() as chars:
    POSS_DIGITS = chars.read()

def convert_dual_base_denary(num:str, outerBase:int, innerBase:int) -> str:
	#Convert a number from a dual base to denary
	innerSize = int(log(outerBase, innerBase))

	num = list(num)

	while len(num) % innerSize != 0:
		num.insert(0, '0')

	#Splits the list into segments of length innerSize
	numArr = [num[i:i + innerSize] for i in range(0, len(num), innerSize)]

	decNumArr = []
	decNum = 0

	#Get the decimal values of all of the digits
	for innerBaseNum in numArr:
		decNumArr.append(convert_denary(innerBaseNum, innerBase))
	decNumArr.reverse()

	#Add the decimal values to the answer, multiplying by the base raised to the power equal to the column number
	for i, num in enumerate(decNumArr):
		decNum += num * (outerBase**i)

	return decNum

def convert_from_dual_base(num:str, outerBase:int, innerBase:int, ansBase:int) -> str:
	#Convert a number from a dual base to any other base
	decNum = convert_dual_base_denary(num, outerBase, innerBase)
	ans = convert_base(str(decNum), 10, ansBase)
	return ans

def convert_to_dual_base(num:str, base:int, ansOuterBase:int, ansInnerBase:int) -> str:
	#Convert a number from any base to a dual base
	innerSize = int(log(ansOuterBase, ansInnerBase))
	ans = ''

	#Convert the number to the outer base
	outerBaseNum = convert_base(num, base, ansOuterBase)

	#Convert each digit to the inner base
	for digit in outerBaseNum:
		output = convert_base(digit, ansOuterBase, ansInnerBase)
		while len(output) < innerSize:
			output = '0' + output
		ans += output

	return ans

def convert_between_dual_bases(num:str, outerBase:int, innerBase:int, ansOuterBase:int, ansInnerBase:int) -> str:
	temp = convert_from_dual_base(num, outerBase, innerBase, 128)
	return convert_to_dual_base(temp, 128, ansOuterBase, ansInnerBase)

def convert_denary(num:str, base:int) -> str:
	#Set up variables
	decNum = 0
	decNumArr = []
	usedDigits = []

	num = num[::-1]

	for i, digit in enumerate(num):
		decNumArr.append(POSS_DIGITS.index(digit) * (base**i))

	decNumArr.reverse()

	for i in decNumArr:
		decNum += i

	return decNum

def convert_base(num:int|str, base:int|str=10, ansBase:int|str=10) -> str:
    """Convert a number from one base to another.

    Arguments:
    num -- the number to be converted (currently only accepts integers)
    base -- the base of the supplied number (default 10)
    ansBase -- the base of the returned number (default 10)
    """
    print(f'converting {num} from {base} to {ansBase}') #debug
    num = str(num)
    
    # Use correct conversion function for dual bases
    if '/' in str(base):
        base = base.split('/')
        if '/' in ansBase:
            ansBase = ansBase.split('/')
            return convert_between_dual_bases(num, int(base[0]), int(base[1]), int(ansBase[0]), int(ansBase[1]))
        else:
            return convert_from_dual_base(num, int(base[0]), int(base[1]), ansBase)
    elif '/' in str(ansBase):
        ansBase = ansBase.split('/')
        return convert_to_dual_base(num, base, int(ansBase[0]), int(ansBase[1]))
            
	#Set up variables
    base = int(base)
    decNum = convert_denary(num, base)
    usedDigits = []
    ansDigits = []
    ans = ''

	#Create an array with the digits of the highest base
    if base > ansBase:
        maxBase = base
    else:
        maxBase = ansBase

    for i in range(maxBase):
        usedDigits.append(POSS_DIGITS[i])

    for digit in num:
        if digit not in usedDigits:
            raise ValueError(f'digit {digit} is not in base {base}')


    #Fix the 'missing zero' error
    if not decNum:
        ansDigits = [0]

	#Succesive division of the denary number by the base with the remainder appended to the answer
    while decNum:
        ansDigits.append(decNum % ansBase)
        decNum //= ansBase

    ansDigits.reverse()

	#Converting each digit from denary to its value in the given base
    for i, digit in enumerate(ansDigits):
        ansDigits[i] = usedDigits[digit]

	#Combining the digits into one string
    for digit in ansDigits:
        ans += digit

    return ans

def detect_base(num:str) -> int:
    """Detect the lowest possible base for a given number

    Arguments:
    num -- the number to be analysed
    """
    base = 0
    for char in num:
        if POSS_DIGITS.index(char) > base: base = POSS_DIGITS.index(char)
    return base
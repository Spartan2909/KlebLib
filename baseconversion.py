from math import log

def convertDenary(num, base):
    #Set up variables
    decNum = 0
    decNumArr = []
    usedDigits = []
    possDigits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ@#£&%;:€$¥_^§|~ςερτυθιοσδφγξλζψωβцгшщзфлджэячиьбюъ'
  
    #Create an array with the digits of the highest base
    if base > 10:
    	maxBase = base
    else:
    	maxBase = 10
  
    for i in range(maxBase):
    	usedDigits.append(possDigits[i])
   
    for digit in num:
    	if digit not in usedDigits:
      		raise ValueError(f'digit {digit} is not in base {base}')
   
    num = num[::-1]
    
    for i, digit in enumerate(num):
    	decNumArr.append(
      		usedDigits.index(digit) * (base ** i)
    	)
    
    decNumArr.reverse()
    
    for i in decNumArr:
    	decNum += i
    
    return decNum
  
def convertBase(num, base, ansBase):
    #Set up variables
    decNum = convertDenary(num, base)
    usedDigits = []
    ansDigits = []
    ans = ''
    possDigits = '01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ@#£&%;:€$¥_^§|~ςερτυθιοσδφγξλζψωβцгшщзфлджэячиьбюъ'
  
    #Create an array with the digits of the highest base
    if base > ansBase:
    	maxBase = base
    else:
    	maxBase = ansBase
  
    for i in range(maxBase):
    	usedDigits.append(possDigits[i])
    
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

def convertDualBaseDenary(num, outerBase, innerBase):
    #Convert a number from a dual base to denary
    innerSize = log(outerBase, innerBase)
    
    num = list(num)

    while len(num) % innerSize:
        num.insert(0, '0')
    
    #Splits the list into segments of length innerSize
    numArr = [num[i:i+innerSize] for i in range(0, len(num), innerSize)] #Don't touch this
    
    decNumArr = []
    decNum = 0

    #Get the decimal values of all of the digits
    for innerBaseNum in numArr:
        decNumArr.append(convertDenary(innerBaseNum, innerBase))
    decNumArr.reverse()

    #Add the decimal values to the answer, multiplying by the base raised to the power equal to the column number
    for i, num in enumerate(decNumArr):
        decNum += num * (outerBase ** i)

    return decNum

def convertFromDualBase(num, outerBase, innerBase, ansBase):
    #Convert a number from a dual base to any other base
    innerSize = log(outerBase, innerBase)
    decNum = convertDualBaseDenary(num, outerBase, innerBase, innerSize)
    ans = convertBase(str(decNum), 10, ansBase)
    return ans

def convertToDualBase(num, base, ansOuterBase, ansInnerBase):
    #Convert a number from any base to a dual base
    innerSize = log(ansOuterBase, ansInnerBase)
    decNum = convertDenary(num, base)
    ansArr = []
    ans = ''

    #Convert the number to the outer base
    outerBaseNum = convertBase(num, base, ansOuterBase)

    #Convert each digit to the inner base
    for digit in outerBaseNum:
        ans += convertBase(digit, ansOuterBase, ansInnerBase)

    return ans

def convertBetweenDualBases(num, outerBase, innerBase, ansOuterBase, ansInnerBase):
    innerSize = log(outerBase, innerBase)
    ansInnerSize = log(ansOuterBase, ansInnerBase)
    temp = convertFromDualBase(num, innerBase, outerBase, innerSize, 6)
    return convertToDualBase(temp, 6, ansInnerBase, ansOuterBase, ansInnerSize)

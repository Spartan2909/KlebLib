from math import log

possDigits = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz@#£&%;:€$¥_^§|~<>()[]{}.,!?ςερτυθιοσδφγξλζψωβцгшщзфлджэячиьбюъ'

def convertDenary(num, base):
    #Set up variables
    decNum = 0
    decNumArr = []
    usedDigits = []
  
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
    innerSize = int(log(outerBase, innerBase))
    
    num = list(num)

    while len(num) % innerSize:
        num.insert(0, '0')
    
    #Splits the list into segments of length innerSize
    numArr = [num[i:i+innerSize] for i in range(0, len(num), innerSize)]
    
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
    innerSize = int(log(outerBase, innerBase))
    decNum = convertDualBaseDenary(num, outerBase, innerBase)
    ans = convertBase(str(decNum), 10, ansBase)
    return ans

def convertToDualBase(num, base, ansOuterBase, ansInnerBase):
    #Convert a number from any base to a dual base
    innerSize = int(log(ansOuterBase, ansInnerBase))
    decNum = convertDenary(num, base)
    ansArr = []
    ans = ''

    #Convert the number to the outer base
    outerBaseNum = convertBase(num, base, ansOuterBase)

    #Convert each digit to the inner base
    for digit in outerBaseNum:
        output = convertBase(digit, ansOuterBase, ansInnerBase)
        while len(output) < innerSize:
            output = '0' + output
        ans += output

    return ans

def convertBetweenDualBases(num, outerBase, innerBase, ansOuterBase, ansInnerBase):
    innerSize = int(log(outerBase, innerBase))
    ansInnerSize = int(log(ansOuterBase, ansInnerBase))
    temp = convertFromDualBase(num, outerBase, innerBase, 6)
    return convertToDualBase(temp, 6, ansOuterBase, ansInnerBase)
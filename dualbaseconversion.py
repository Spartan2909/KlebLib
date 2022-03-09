#Caleb Robson

from baseConversion import *

def convertDualBaseDenary(num, innerBase, outerBase, innerSize):
    #Convert a number from a dual base to denary
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

def convertFromDualBase(num, innerBase, outerBase, innerSize, ansBase):
    #Convert a number from a dual base to any other base
    decNum = convertDualBaseDenary(num, innerBase, outerBase, innerSize)
    ans = convertBase(str(decNum), 10, ansBase)
    return ans

def convertToDualBase(num, base, ansInnerBase, ansOuterBase, innerSize):
    #Convert a number from any base to a dual base
    decNum = convertDenary(num, base)
    ansArr = []
    ans = ''

    #Convert the number to the outer base
    outerBaseNum = convertBase(num, base, ansOuterBase)

    #Convert each digit to the inner base
    for digit in outerBaseNum:
        ans += convertBase(digit, ansOuterBase, ansInnerBase)

    return ans
from baseconversion import *
from dualbaseconversion import *

def add(base, *nums):
    #Check validity of input
    if not isinstance(base, int):
        raise ValueError(f'Expected int, got {type(base)}')
    
    #Set up nums
    nums = list(nums)
    if len(nums) < 2:
        raise ValueError('List nums must be of length 2 or greater')
  
    #print(f'{nums} start') #debug

	#Add the first 2 numbers, store the value as the first num and delete the second num
    while len(nums) > 2:
        #print('recursion activated') #debug
        nums[0] = addNums(base, nums[0], nums[1])
        del nums[1]
  
    #print(f'{nums} passed while loop') #debug
  
    num1 = nums[0]
    num2 = nums[1]
  
    #Set up variables
    carry = 0
    result = 0
    answer = []
    convertedAns = []
    finalAns = ''
    num1arr = []
    num2arr = []
  
    #Turn the strings into lists
    for (num1digit, num2digit) in zip(num1, num2):
        num1arr.append(num1digit)
        num2arr.append(num2digit)
    num1 = num1arr
    num2 = num2arr
  
    #Reverse the arrays and equalise the lengths
    num1.reverse()
    num2.reverse()
  
    while len(num1) != len(num2):
        if len(num1) > len(num2):
            num2.append('0')
    else:
      num1.append('0')
    
    #Convert nums to denary and add the numbers    
    for i, (num1digit, num2digit) in enumerate(zip(num1, num2)):
        num1digit = int(convertDenary(num1digit, base))
        num1[i] = num1digit
        num2digit = int(convertDenary(num2digit, base))
        num2[i] = num2digit
		
        result = num1digit + num2digit + carry
        if result >= carry:
        	carry = result // base
        	result = int(result % base)
        answer.append(result)
        print(f'result: {result}') #debug
        print(f'carry: {carry}') #debug
    
    #Handle overflow
    if carry > 0:
    	answer.append(carry)
    
    #Reverse answer to be in the correct order
    #print(f'reverse list answer: {answer}') #debug
    answer.reverse()
    #print(f'list answer: {answer}') #debug
  
    #Convert digits to string
    for i in range(len(answer)):
        answer[i] = str(answer[i])
    #print(f'string list answer: {answer}') #debug
 
    #Convert answer back to original base
    for i in range(len(answer)):
        convertedAns.append(convertBase(answer[i], 10, base))
    #print(f'converted answer: {convertedAns}') #debug
	
    #Combine digits into one string
    for i in convertedAns:
    	finalAns += str(i)
    
    return finalAns
  
def convertListDenary(num, base):
    for i in range(len(num)):
    	num[i] = int(convertDenary(str(num[i]), base))
    return num
    
def convertListUnknown(num, base):
    convertedAns = []
    for i in range(len(num)):
    	convertedAns.append(convertBase(answer[i], 10, base))
    #print(f'converted answer: {convertedAns}') #debug
  
    #Correct blank digits to 0s
    for i in range(len(convertedAns)):
        if not convertedAns[i]:
            convertedAns[i] = '0'
    #print(f'corrected answer: {convertedAns}') #debug
  
    return convertedAns

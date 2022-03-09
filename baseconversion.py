#Caleb Robson and Kai Kerlaff

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
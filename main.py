import re

class Fraction:
    def __init__(self, fraction, listInput=False):
        if listInput:
            self.num = fraction[0]
            self.dem = fraction[1]
        else:
            fraction_nums = fraction.split('/')
            map_object = map(int, fraction_nums)
            fraction_nums = list(map_object)        
            self.num = fraction_nums[0]
            self.dem = fraction_nums[1]

        simplified = [x/self.GCD() for x in [self.num, self.dem]]
        if [self.num, self.dem] != simplified:
            self.simplify()

    #Get the greatest common divisor of the numerator and denominator
    def GCD(self):
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

        return num2

    #Simplify the fraction
    def simplify(self):
        GCD = self.GCD()

        self.num = int(self.num / GCD)
        self.dem = int(self.dem / GCD)
            
    #Automatically simplify fractions
    #Entirely nonfunctional
    def autoSimplify(self, func):
        def inner(*args, **kwargs):
            fraction = func(*args, **kwargs)
            fraction.simplify
            return fraction
            
        return inner
  
    #Output the numbers as a fraction     
    def output(self):
        return(f'{self.num}/{self.dem}')
  
    #Output the fraction as a float  
    def outputFloat(self):
        return self.num/self.dem
  
    #Adds another fraction to this one
    def addFraction(self, fraction2):
        num = (self.num * fraction2.dem) + (self.dem * fraction2.num)
        dem = self.dem * fraction2.dem

        result = Fraction([num, dem], True)
        result.simplify()
        return result
  
    #Subtracts another fraction from this one  
    def subFraction(self, fraction2):
        num = (self.num * fraction2.dem) - (self.dem * fraction2.num)
        dem = self.dem * fraction2.dem

        result = Fraction([num, dem], True)
        result.simplify()
        return result
  
    #Multiplies this fraction by another one 
    def timesFraction(self, fraction2):
        num = self.num * fraction2.num
        dem = self.dem * fraction2.dem

        result = Fraction([num, dem], True)
        result.simplify()
        return result
  
    #Divides this fraction by another one  
    def divFraction(self, fraction2):
        num = self.num * fraction2.dem
        dem = self.dem * fraction2.num

        result = Fraction([num, dem], True)
        result.simplify()
        return result

    #Returns a mixed fraction
    def balance(self, listOutput=False):
        integerPart = 0
        num = self.num
        dem = self.dem

        while num > dem:
            num -= dem
            integerPart += 1

        if listOutput:
            return [integerPart, [num, dem]]
        else:
            return f'{integerPart} {num}/{dem}'
    
    #return a list of the numerator and denominator
    def nums(self):
        return([self.num, self.dem])

class Polynomial:
    def __init__(self, polynomial, dictInput=False):
        if dictInput:
            self.polynomial = polynomial
        else:
            self.polynomial = self.parse(polynomial)

    def parse(self, polynomaial):
        negatives = []
        additions = re.finditer('\+|-', polynomial)
        startNegative = re.search('^\+|-', polynomial)

        for i, match in enumerate(additions):
            if match.group() == '-':
                if startNegative:
                    negatives.append(i)
                else:
                    negatives.append(i + 1)

        terms = re.split('\+|-', polynomial)
        if startNegative:
            del terms[0]

        polynomial = {}
        for i, term in enumerate(terms):
            terms[i] = term.strip()
            term = terms[i]
            print(term)

            #Check if term should be negative
            if i in negatives:
                negativeMultiple = -1
            else:
                negativeMultiple = 1

            if 'x' in term:
                if '^' in term:
                    term = term.split('x^')
                    try:
                        polynomial[float(term[1])] = float(term[0]) * negativeMultiple
                    except ValueError:
                        polynomial[float(term[1])] = 1 * negativeMultiple
                else:
                    term = term[:-1]
                    polynomial[1] = float(term) * negativeMultiple
            else:
                polynomial[0] = float(term) * negativeMultiple

        return polynomial

    def differentiate(self):
        polynomial = {}
        for exponent, coefficient in self.polynomial.items():
            polynomial[exponent - 1] = coefficient * exponent

        return polynomial

    def integrate(self):
        polynomial = {}
        for exponent, coefficient in self.polynomial.items():
            polynomial[exponent + 1] = coefficient / (exponent + 1)

        return polynomial

    def output(self):
        #TODO output in readable format
        return self.polynomial

def test(testType, **kwargs):
    if testType == 'fraction':
        return fractionTest(kwargs)
    elif testType == 'polynomial':
        return polynomialTest(kwargs)

def fractionTest(kwargs):
    fraction1 = Fraction(kwargs['fraction1'])
    fraction2 = Fraction(kwargs['fraction2'])

    opType = kwargs['opType']
    if opType == 'add':
        fraction3 = fraction1.addFraction(fraction2)
    elif opType == 'subtract':
        fraction3 = fraction1.subFraction(fraction2)
    elif opType == 'multiply':
        fraction3 = fraction1.timesFraction(fraction2)
    elif opType == 'divide':
        fraction3 = fraction1.divFraction(fraction2)

    return fraction3.output()

def polynomialTest(polynomial, listInputBool):
    polynomial = Polynomial(polynomial, listInput=listInputBool)

    differentiated = polynomial.differentiate()
    integrated = polynomial.integrate()

    return [differentiated.output(), integrated.output()]
    
def ceiling(num, decPlaces):
    #Set up variables
    overflow = False
    num = str(num)
    numDigits = []
    for digit in num:
        numDigits.append(digit)
    decPoint = numDigits.index('.')
  
    #Removes the decimal point and finds the last decimal place that will remain
    del numDigits[decPoint]
    lastPlace = decPoint + decPlaces - 1
  
    #Turns all of the digits into int
    for i, digit in enumerate(numDigits):
        numDigits[i] = int(digit)
  
    #Rounds up
    complete = False
    roundMod = 0
    while not complete:
        if numDigits[lastPlace - roundMod] < 9:
            numDigits[lastPlace - roundMod] += 1
            complete = True
        else:
            if numDigits[lastPlace] - roundMod - 1 < 0:
                numDigits.insert(0, 1)
                complete = True
                overflow = True
            else:
                numDigits[lastPlace - roundMod] = 0
                roundMod += 1
    
    #Remove the extra digits
    while len(numDigits) > lastPlace + 1:
        del numDigits[lastPlace + 1]
  
    #Reformats and outputs the answer   
    numDigits.insert(decPoint + int(overflow), '.')
    num = ''
    for i in numDigits:
        num += str(i)
    num = float(num)
    return num

def smartRound(num, decPlaces):
    pass

if __name__ == '__main__':
    test1 = test('fraction', fraction1='1/2', fraction2='4/5', opType='add')
    print(test1)
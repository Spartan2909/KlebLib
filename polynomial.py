import re

class Polynomial:
    def __new__(cls, polynomials, dictInput=False):
        if (dictInput and isinstance(list(polynomials.values())[0], dict)) or (len(cls.getVariables(polynomials)) > 1):
            return MultiVarPolynomial(polynomials, dictInput=dictInput)
        else:
            return SingleVarPolynomial(polynomials, dictInput=dictInput)

    def getVariables(polynomial):
        variables = set()
        try:
            for character in polynomial:
                #If it is a letter
                if (ord(character) >= 65 and ord(character) <= 90) or (ord(character) >= 97 and ord(character) <= 122):
                    variables.add(character)
        #If polynomial is not a string
        except:
            return []

        return list(variables)

class SingleVarPolynomial:
    def __init__(self, polynomial, dictInput=False):
        if dictInput:
            if not isinstance(polynomial, dict):
                raise ValueError(f'Expected dict, got {type(polynomial)}')
            self.polynomial = polynomial
        else:
            if not isinstance(polynomial, str):
                raise ValueError(f'Expected str, got {type(polynomial)}')
            variable = Polynomial.getVariables(polynomial)[0]
            self.polynomial = self.parse(polynomial, variable)

    def parse(self, polynomial, variable):
        #print(f'parsing polynomial {polynomial}') #debug
        negatives = []
        additions = re.finditer(r'[\+-]', polynomial)
        startNegative = re.search(r'^[\+-]', polynomial)

        for i, match in enumerate(additions):
            if match.group() == '-':
                if startNegative:
                    negatives.append(i)
                else:
                    negatives.append(i + 1)

        terms = re.split(r'[\+-]', polynomial)
        if startNegative:
            #print('removed first term') # debug
            del terms[0]

        polynomial = {}
        for i, term in enumerate(terms):
            terms[i] = term.strip()
            term = terms[i]
            #print(f'parsing term {term}') #debug

            #Check if term should be negative
            if i in negatives:
                negativeMultiple = -1
            else:
                negativeMultiple = 1

            if variable in term:
                if '^' in term:
                    term = term.split(f'{variable}^')
                    try:
                        polynomial[float(term[1])] = float(term[0]) * negativeMultiple
                    except ValueError: #If there is no coefficient
                        polynomial[float(term[1])] = negativeMultiple
                else: #If it has no exponent
                    term = term[:-1]
                    if term: #If there is a coefficient
                        polynomial[1] = float(term) * negativeMultiple
                    else:
                        polynomial[1] = 1
            else: #If it is just a number
                polynomial[0] = float(term) * negativeMultiple

            #print(f'parsed term {term}') #debug

        return polynomial

    def differentiate(self):
        polynomial = {}
        for exponent, coefficient in self.polynomial.items():
            if coefficient * exponent != 0:  #If the coefficient will not be 0
                polynomial[exponent - 1] = coefficient * exponent

        return Polynomial(polynomial, True)

    def integrate(self):
        polynomial = {}
        for exponent, coefficient in self.polynomial.items():
            polynomial[exponent + 1] = coefficient / (exponent + 1)

        return Polynomial(polynomial, True)

    def integrateDefinite(self, min, max):
        expr = self.integrate()
        upper = lower = 0

        for exponent, coefficient in expr.items():
            upper += coefficient * max ** exponent
            lower += coefficient * min ** exponent

        result = max - min
        return result

    def __add__(self, other):
        if isinstance(other, SingleVarPolynomial):
            returnPolynomial = self.polynomial.copy()
            for exponent, coefficient in other.polynomial.items():
                if exponent in returnPolynomial.keys():
                    returnPolynomial[exponent] += coefficient
                else:
                    returnPolynomial[exponent] = coefficient
    
            return Polynomial(returnPolynomial, True)
        else:
            outputPolynomial = other.polynomials.copy()
            if Polynomial.getVariables(self.polynomial)[0] in other.polynomials:
                pass
            else:
                outputPolynomial[Polynomial.getVariables(self.polynomial)[0]] = self.polynomial
                return Polynomial(outputPolynomial, True)

    def __sub__(self, other):
        if isinstance(other, SingleVarPolynomial):
            returnPolynomial = self.polynomial.copy()
            for exponent, coefficient in other.polynomial.items():
                if exponent in returnPolynomial.keys():
                    returnPolynomial[exponent] -= coefficient
                else:
                    returnPolynomial[exponent] = -coefficient
    
            return Polynomial(returnPolynomial, True)
        else:
            outputPolynomial = other.polynomials.copy()
            if Polynomial.getVariables(self.polynomial)[0] in other.polynomials:
                pass
            else:
                pass

    def __iadd__(self, other):
        if isinstance(other, SingleVarPolynomial):
            for exponent, coefficient in other.polynomial.items():
                if exponent in self.polynomial.keys():
                    self.polynomial[exponent] += coefficient
                else:
                    self.polynomial[exponent] = coefficient
    
            return self
        else:
            raise TypeError('Cannot implicitly convert single variable polynomial to multi variable polynomial. Try using \'this = this + other\' instead')

    def __isub__(self, other):
        if isinstance(other, SingleVarPolynomial):
            for exponent, coefficient in other.polynomial.items():
                if exponent in self.polynomial.keys():
                    self.polynomial[exponent] -= coefficient
                else:
                    self.polynomial[exponent] = -coefficient
    
            return self
        else:
            raise TypeError('Cannot implicitly convert single variable polynomial to multi variable polynomial. Try using \'this = this + other\' instead')

    def output(self, readable=False):
        if readable:
            output = ''
            i = 0
            for exponent, coefficient in self.polynomial.items():
                if coefficient < 0:
                    if i == 0:
                        output += '-'
                    else:
                        output += ' - '
                elif i != 0:
                    output += ' + '

                if exponent > 1 or exponent < 0:
                    output += f'{abs(coefficient)}x^{exponent}'
                elif exponent == 1:
                    output += f'{abs(coefficient)}x'
                else:
                    output += f'{abs(coefficient)}'

                i += 1

            return output
        else:
            return self.polynomial

class MultiVarPolynomial:
    def __init__(self, polynomials, dictInput=False):
        #print(f'the polynomials are {polynomials} and are of type {type(polynomials)}') #debug
        #print(f'dictInput is {dictInput}') #debug
        if dictInput:
            self.polynomials = polynomials
        else:
            self.polynomials = self.parse(polynomials, Polynomial.getVariables(polynomials))

        #print(self.polynomials) #debug

    def parse(self, polynomial, variables):
        print(f'multivar parsing {polynomial} with variables {variables}') #debug

        output = {}
        negativesList = []
        negatives = {}
        additions = re.finditer(r'[\+-]', polynomial)
        startNegative = re.search(r'^[\+-]', polynomial)

        for i, match in enumerate(additions):
            if match.group() == '-':
                if startNegative:
                    negativesList.append(i)
                else:
                    negativesList.append(i + 1)

        termsList = re.split(r'[\+-]', polynomial)
        if startNegative:
            #print('removed first term') # debug
            del terms[0]
        terms = {}
        for variable in variables:
            terms[variable] = []
            negatives[variable] = []
            lenCurrentTerms = 0
            
            for i, term in enumerate(termsList):
                if variable in term:
                    terms[variable].append(term.strip())
                    if i in negativesList:
                        negatives[variable].append(lenCurrentTerms)
                    lenCurrentTerms += 1

        terms['nums'] = []
        negatives['nums'] = []
        lenCurrentTerms = 0
        
        for i, term in enumerate(termsList):
            try:
                float(term)
            except ValueError:
                pass
            else:
                terms['nums'].append(term)
                if i in negativesList:
                    negatives['nums'].append(lenCurrentTerms)
                lenCurrentTerms += 1

        #print(f'the terms are {terms}') #debug
        #print(f'the negatives are {negatives}') #debug

        for variable, varTerms in terms.items():
            print(f'parsing variable {variable} with terms {varTerms}')
            if variable == 'nums':
                output[variable] = []
            else:
                output[variable] = {}
            if i in negatives[variable]:
                negativeMultiple = -1
            else:
                negativeMultiple = 1
            
            for term in varTerms:
                if variable in term:
                    if '^' in term:
                        term = term.split(f'{variable}^')
                        try:
                            output[variable][float(term[1])] = float(term[0]) * negativeMultiple
                        except ValueError: #If there is no coefficient
                            output[variable][float(term[1])] = negativeMultiple
                    else: #If it has no exponent
                        term = term[:-1]
                        if term: #If there is a coefficient
                            output[variable][1] = float(term) * negativeMultiple
                        else:
                            output[variable][1] = 1
                else: #If it is just a number
                    output[variable].append(float(term) * negativeMultiple)

        return output
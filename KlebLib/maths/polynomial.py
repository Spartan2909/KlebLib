"""Polynomial -- store and manipulate polynomials"""

import re
from copy import deepcopy
from .fraction import Fraction

__all__ = ['Polynomial']

class Term:
    def __init__(self, term:str|list):
        if type(term) is str:
            term = term.split('^')
        
        self.value = term[0]
        self.exp = term[1]

    def __add__(self, value):
        if re.search('[+-]\s\d+', self.value):
            value += Polynomial.trim_num(self.value, 'right')
        
        self.value += f' + {value}'

    def __sub__(self, value):
        if re.search('[+-]\s\d+', self.value):
            value += Polynomial.trim_num(self.value, 'right')
        
        self.value += f' - {value}'

    def copy(self):
        return Term([self.value, self.exp])

class Polynomial:
    """Store a polynomial as a list of terms.

    Methods:
    differentiate(varToDiff) -- differentiates the polynomial with respect to varToDiff. if no variable is supplied, and the polynomial only has a single variable, that will be used instead
    integrate(varToIntegrate) -- integrates the polynomial with respect to varToIntegrate. if no variable is supplied, and the polynomial only has a single variable, that will be used instead
    integrate_definite(varToIntegrate)
    """
    def __init__(self, polynomial:str|list):
        #print(f'the polynomials are {polynomial} and are of type {type(polynomial).__name__}') #debug
        if type(polynomial) is list:
            for term in polynomial:
                if not 'num' in term:
                    term['num'] = 1
            self.polynomial = polynomial
        else:
            self.polynomial = Polynomial.parse(polynomial)
        #print(self.polynomial) #debug

    def differentiate(self, varToDiff:str=None, degree:int=1):
        if varToDiff is None:
            #print(f'attempting to imply variable from polnomial with variables {self.get_variables(self.polynomial)}') #debug
            if len(Polynomial.get_variables(self.polynomial)) != 1:
                raise ValueError('cannot implicitly detect variable for polynomials of multiple variables')
            else:
                varToDiff = Polynomial.get_variables(self.polynomial)[0]

        startPolynomial = deepcopy(self.polynomial)
        for _ in range(degree):
            outputPolynomial = []
            for term in startPolynomial:
                termToEdit = {}
                edited = False
                for variable, exponent in term.items():
                    if variable == varToDiff:
                        termToEdit['num'] = term['num'] * exponent
                        if exponent - 1 != 0:
                            termToEdit[variable] = exponent - 1
                        edited = True
                    elif variable != 'num':
                        termToEdit[variable] = exponent
                if edited:
                    outputPolynomial.append(termToEdit)

            startPolynomial = outputPolynomial.copy()

        return Polynomial(outputPolynomial)

    def integrate(self, varToIntegrate:str=None, degree:int=1):
        if varToIntegrate is None:
            if len(Polynomial.get_variables(self.polynomial)) != 1:
                raise ValueError('cannot implicitly detect variable for polynomials of multiple variables')
            else:
                varToIntegrate = Polynomial.get_variables(self.polynomial)[0]

        startPolynomial = deepcopy(self.polynomial)
        for _ in range(degree):
            outputPolynomial = []
            for term in startPolynomial:
                termToEdit = {}
                edited = False
                for variable, exponent in term.items():
                    if variable == varToIntegrate:
                        termToEdit['num'] = term['num'] / (exponent + 1)
                        termToEdit[variable] = exponent + 1
                        edited = True
                    elif variable != 'num':
                        termToEdit[variable] = exponent
                if not edited:
                    termToEdit['num'] = term['num']
                    termToEdit[varToIntegrate] = 1
    
                outputPolynomial.append(termToEdit)

            startPolynomial = outputPolynomial.copy()

        return Polynomial(outputPolynomial)

    def integrate_definite(self, varToIntegrate:str, max:int, min:int, degree:int=1):
        integrated = self.integrate(varToIntegrate, degree)
        outputs = [[], []]
        limits = [max, min]

        for i, output in enumerate(outputs):
            for term in integrated.polynomial:
                outputTerm = {}
                edited = False
                for variable, exponent in term.items():
                    if variable == varToIntegrate:
                        outputTerm['num'] = term['num'] * limits[i] ** exponent
                        edited = True
                    elif variable != 'num':
                        outputTerm[variable] = exponent

                if not edited:
                    outputTerm['num'] = term['num']

                output.append(outputTerm)

            #print(f'output {i} before cleanup is {output}') #debug
            output = Polynomial.consolidate(output)
            #print(f'output {i} after cleanup is {output}') #debug

        upper = Polynomial(outputs[0])
        lower = Polynomial(outputs[1])

        return upper - lower

    def __add__(self, other):
        #print(f'adding polynomials {self} and {other}') #debug
        outputPolynomial = deepcopy(self.polynomial)
        
        for i, term in enumerate(deepcopy(other.polynomial)):
            #print(f'adding term {term} to polynomial {outputPolynomial}') #debug
            location = Polynomial.locate(outputPolynomial.copy(), term.copy())
            if location is not None:
                outputPolynomial[location]['num'] += term['num']
            else:
                outputPolynomial.append(term.copy())

        #print(f'finished polynomial is {self.consolidate(outputPolynomial)}') #debug
        return Polynomial(Polynomial.consolidate(outputPolynomial))

    def __sub__(self, other):
        #print(f'subtracting polynomial {other} from {self}') #debug
        outputPolynomial = deepcopy(self.polynomial)
        
        for i, term in enumerate(deepcopy(other.polynomial)):
            #print(f'subtracting term {term} from polynomial {outputPolynomial}') #debug
            location = Polynomial.locate(outputPolynomial.copy(), term.copy())
            if location is not None:
                outputPolynomial[location]['num'] -= term['num']
            else:
                currentTerm = {}
                for variable, exponent in term.items():
                    if variable == 'num':
                        currentTerm['num'] = -exponent
                    else:
                        currentTerm[variable] = exponent
                outputPolynomial.append(currentTerm)

        #print(f'finished polynomial is {self.consolidate(outputPolynomial)}') #debug
        return Polynomial(Polynomial.consolidate(outputPolynomial))

    def __iadd__(self, other):
        #print(f'adding polynomials {self} and {other}') #debug
        outputPolynomial = deepcopy(self.polynomial)
        
        for i, term in enumerate(deepcopy(other.polynomial)):
            #print(f'adding term {term} to polynomial {outputPolynomial}') #debug
            location = Polynomial.locate(outputPolynomial.copy(), term.copy())
            if location is not None:
                outputPolynomial[location]['num'] += term['num']
            else:
                outputPolynomial.append(term.copy())

        #print(f'finished polynomial is {self.consolidate(outputPolynomial)}') #debug
        self.polynomial = Polynomial.consolidate(outputPolynomial)
        return self

    def __isub__(self, other):
        #print(f'subtracting polynomial {other} from {self}') #debug
        outputPolynomial = deepcopy(self.polynomial)
        
        for i, term in enumerate(deepcopy(other.polynomial)):
            #print(f'suntracting term {term} from polynomial {outputPolynomial}') #debug
            location = Polynomial.locate(outputPolynomial.copy(), term.copy())
            if location is not None:
                outputPolynomial[location]['num'] -= term['num']
            else:
                currentTerm = {}
                for variable, exponent in term.items():
                    if variable == 'num':
                        currentTerm['num'] = -exponent
                    else:
                        currentTerm[variable] = exponent
                outputPolynomial.append(currentTerm)

        #print(f'finished polynomial is {self.consolidate(outputPolynomial)}') #debug
        self.polynomial = Polynomial.consolidate(outputPolynomial)
        return self

    def __str__(self):
        output = ''

        i = 0
        for term in self.polynomial:
            if term['num'] == 0:
                continue
            elif term['num'] < 0:
                if term['num'] != -1:
                    if i == 0:
                        output += f'-{int_if_pos(abs(term["num"]))}'
                    else:
                        output += f' - {int_if_pos(abs(term["num"]))}'
                else:
                    if i == 0:
                        output += '-'
                    else:
                        output += ' - '
            elif i != 0:
                if term['num'] == 1:
                    output += ' + '
                else:
                    output += f' + {int_if_pos(term["num"])}'
            elif term['num'] != 1:
                output += str(int_if_pos(term['num']))

            i += 1
                
            for variable, exponent in term.items():
                if variable != 'num':
                    if exponent == 1:
                        output += str(variable)
                    else:
                        output += variable + translate_to_super(int_if_pos(exponent))

        if not output:
            output = '0'
                
        return output

    def __repr__(self):
        return f'KlebLib.maths.polynomial.Polynomial({self.polynomial})'

    def __float__(self):
        temp = self.polynomial[0].copy()
        del temp['num']
        
        if len(self.polynomial) == 1 and not temp:
            return float(self.polynomial[0]['num'])
        else:
            raise ValueError('cannot convert polynomial with variables to float')

    def __int__(self):
        try:
            return int(float(self))
        except ValueError:
            raise ValueError('cannot convert polynomial with variables to int')

    def __getitem__(self, variable):
        output = []
        
        for term in self.polynomial:
            if variable in term:
                output.append(term.copy())

        return Polynomial(output)

    def __eq__(self, other):
        equal = True

        for term in self.polynomial:
            #print(f'comparing term {term} from self') #debug
            if term not in other.polynomial:
                #print(f'didn\'t find term {term} in other') #debug
                equal = False
                
        for term in other.polynomial:
            #print(f'comparing term {term} from other') #debug
            if term not in self.polynomial:
                #print(f'didn\'t find term {term} in self') #debug
                equal = False

        return equal

    @staticmethod
    def parse(polynomial:str) -> list:
        #parse the polynomial into a list of dictionaries
        
        #print(f'parsing polynomial {polynomial}') #debug
        output = []
        negatives = []
        if polynomial[0] == '-':
            negatives.append(0)
            polynomial = polynomial[1:]

        for i, match in enumerate(re.finditer(r'\s+[+-]\s+', polynomial)):
            #print(f'the match at position {i} is {match.group()}') #debug
            if match.group() == ' - ':
                negatives.append(i + 1)

        #print(f'the terms are {[Polynomial.translate_super(i) for i in re.split(r'\s+[+-]\s+', polynomial)]}') #debug
        #print(f'the negatives are {negatives}') #debug

        for i, term in enumerate([translate_from_super(i) for i in re.split(r'\s+[+-]\s+', polynomial)]):
            term = term.strip()
            #print(f'parsing term {term} at position {i}') #debug
            
            currentTerm = {}
                
            #Check if term should be negative
            if i in negatives:
                negativeMultiple = -1
            else:
                negativeMultiple = 1
                        
            for variable in Polynomial.get_variables(term):
                if f'{variable}^' in term:
                    currentTerm[variable] = trim_num(term, 'right')
                            
                else: #If it has no exponent
                    currentTerm[variable] = 1

            trimmed = trim_num(term, 'left')
            if trimmed: #If there is a coefficient
                currentTerm['num'] = trimmed * negativeMultiple
            else:
                currentTerm['num'] = negativeMultiple

            if currentTerm:
                output.append(currentTerm)

        return output

    @staticmethod
    def locate(polynomial:list, searchTerm:dict) -> int:
        #print(f'locating term {searchTerm} in polynomial {polynomial}') #debug
        del searchTerm['num']
        for i, term in enumerate(polynomial):
            termToEdit = term.copy()
            del termToEdit['num']
            if searchTerm == termToEdit:
                #print(f'found term at position {i}') #debug
                return i
        #print('didn\'t find term') #debug
        return None

    @staticmethod
    def consolidate(polynomial:list) -> list:
        output = deepcopy(polynomial)
        termsToRemove = []
        
        total = 0
        for term in output:
            numVars = 0
            for variable in term:
                if variable != 'num':
                    numVars += 1

            if numVars == 0:
                total += term['num']
                termsToRemove.append(term)

        if total:
            output.append({'num': total})

        for term in termsToRemove:
            del output[output.index(term)]

        return output

    @staticmethod
    def get_variables(polynomial:str|list) -> list:
        variables = set()

        if type(polynomial) is str:
            for character in polynomial:
                # If it is not a number
                if character not in [str(i) for i in range(10)] + ['.', '^']:
                    variables.add(character)

        elif type(polynomial) is list:
            for term in polynomial:
                for variable in term:
                    if variable != 'num':
                        variables.add(variable)

        return list(variables)

def int_if_pos(num:int|float|str) -> int|float|str:
    #print(f'checking if {num} can be int') #debug
    try:
        assert int(float(num)) == float(num)
    except AssertionError:
        return float(num)
    else:
        return int(float(num))

def get_num_pos(string:str, side:str) -> list:
    if side == 'left':
        numPos = re.search(r'^-?\d+\.?\d*', string)
    else:
        numPos = re.search(r'-?\d+\.?\d*$', string)

    if numPos:
        return [numPos.start(), numPos.end()]

def trim_num(string:str, side:str) -> float:
        #print(f'trimming {string}') #debug
        numPos = get_num_pos(string, side)

        if numPos:
            #print(f'num found between positions {numPos[0]} and {numPos[1]}') #debug
            return float(string[numPos[0]:numPos[1]])
        else:
            #print(f'num not found') #debug
            return 0.0

def translate(string:str, table:dict) -> str:
        trans = str.maketrans(
            ''.join(table.keys()),
            ''.join(table.values())
        )

        return string.translate(trans)

def translate_to_super(num:str) -> str:
    return translate(str(num), {
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
        "7": "⁷", "8": "⁸", "9": "⁹", "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ",
        "e": "ᵉ", "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ᶦ", "j": "ʲ", "k": "ᵏ",
        "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ", "p": "ᵖ", "q": "۹", "r": "ʳ",
        "s": "ˢ", "t": "ᵗ", "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ",
        "z": "ᶻ", "A": "ᴬ", "B": "ᴮ", "C": "ᶜ", "D": "ᴰ", "E": "ᴱ", "F": "ᶠ",
        "G": "ᴳ", "H": "ᴴ", "I": "ᴵ", "J": "ᴶ", "K": "ᴷ", "L": "ᴸ", "M": "ᴹ",
        "N": "ᴺ", "O": "ᴼ", "P": "ᴾ", "Q": "Q", "R": "ᴿ", "S": "ˢ", "T": "ᵀ",
        "U": "ᵁ", "V": "ⱽ", "W": "ᵂ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ", "+": "⁺",
        "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾"
    })

def translate_from_super(string:str) -> str:
    #print(f'translating {string}') #debug
    string = translate(string, {j: i for i, j in {
        "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
        "7": "⁷", "8": "⁸", "9": "⁹", "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ",
        "e": "ᵉ", "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ᶦ", "j": "ʲ", "k": "ᵏ",
        "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ", "p": "ᵖ", "q": "۹", "r": "ʳ",
        "s": "ˢ", "t": "ᵗ", "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ",
        "z": "ᶻ", "A": "ᴬ", "B": "ᴮ", "C": "ᶜ", "D": "ᴰ", "E": "ᴱ", "F": "ᶠ",
        "G": "ᴳ", "H": "ᴴ", "I": "ᴵ", "J": "ᴶ", "K": "ᴷ", "L": "ᴸ", "M": "ᴹ",
        "N": "ᴺ", "O": "ᴼ", "P": "ᴾ", "Q": "Q", "R": "ᴿ", "S": "ˢ", "T": "ᵀ",
        "U": "ᵁ", "V": "ⱽ", "W": "ᵂ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ", "+": "⁺",
        "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾"
    }.items()})

    num = trim_num(string, 'right')
    numPos = get_num_pos(string, 'right')

    if numPos:
        if numPos[0] == 0:
            return string
        if string[numPos[0] - 1] == '^':
            return string[:numPos[0]] + str(num)
        else:
            return string[:numPos[0]] + '^' + str(num)
    else:
        return string
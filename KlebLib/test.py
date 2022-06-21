from .maths import baseconversion, fraction, polynomial, rounding, universaladdition
from .structures import series, tree

class Test:
    def __init__(self, testType:str, **kwargs):
        self.testType = testType
        self.kwargs = kwargs

    def __call__(self, *args):
        if self.testType == 'fraction':
            print(self.fraction_test(args))
        elif self.testType == 'polynomial':
            print(self.polynomial_test(args))
        elif self.testType == 'baseconversion':
            print(self.conversion_test(args))
        elif self.testType == 'universaladdition':
            print(self.universal_addition_test(args))
        elif self.testType == 'series':
            print(self.series_test(args))

    def __repr__(self):
        output = f'KlebLib.test.Test({self.testType}, '

        #print(f'kwargs are of length {len(self.kwargs)}') #debug
        for i, (k, v) in enumerate(self.kwargs.items()):
            output += f'{k}=\'{v}\''
            if i != len(self.kwargs.keys()) - 1:
                output += ', '

        output += ')'
        return output

    #Individual tests

    def fraction_test(self, args):
        fraction1 = fraction.Fraction(self.kwargs['fraction1'])
        fraction2 = fraction.Fraction(self.kwargs['fraction2'])

        opType = self.kwargs['opType']
        if opType == 'add' or opType == '+':
            fraction3 = fraction1 + fraction2
        elif opType == 'subtract' or opType == '-':
            fraction3 = fraction1 - fraction2
        elif opType == 'multiply' or opType == '*':
            fraction3 = fraction1 * fraction2
        elif opType == 'divide' or opType == '/':
            fraction3 = fraction1 / fraction2

        return str(fraction3)

    def polynomial_test(self, args):
        testPolynomial = polynomial.Polynomial(self.kwargs['polynomial'])

        differentiated = testPolynomial.differentiate(args[0])
        integrated = testPolynomial.integrate(args[0])

        return str({
            'polynomial': testPolynomial.polynomial,
            'readable': str(testPolynomial),
            'differentiated': differentiated.polynomial,
            'integrated': integrated.polynomial
        })

    def conversion_test(self, args):
        num = self.kwargs['num']
        base = self.kwargs['base']
        convertedBase = self.kwargs['baseToConvertTo']

        return baseconversion.convert_base(num, base, convertedBase)

    def universal_addition_test(self, args):
        num1 = self.kwargs['num1']
        num2 = self.kwargs['num2']
        base = self.kwargs['base']

        return universaladdition.add(base, num1, num2)

    def series_test(self, args):
        testSeries = series.Series(self.kwargs['data'], self.kwargs.get('seriesType'), self.kwargs.get('strictType'))
        return str({
            'base series': str(testSeries),
            'base series + arg': str(testSeries.add(args[0]))
        })
# coding=utf-8
"""Test various diamond inheritance."""

class Human(object):

    def say(self):
        print("Say Human")
        print("Said Human")


class Woman(Human):

    def say(self):
        print("Say Woman")
        super(Woman, self).say()
        print("Said Woman")


class Mother(Woman):

    def say(self):
        print("Say Mother")
        super(Mother, self).say()
        print("Said Mother")


class Father(Human):

    def say(self):
        print("Say Father")
        super(Father, self).say()
        print("Said Father")


class Parent(Mother, Father):
    """Fancy parents.

    >>> Parent().say()
    Say Parent
    Say Mother
    Say Woman
    Say Father
    Say Human
    Said Human
    Said Father
    Said Woman
    Said Mother
    Said Parent
    """

    def say(self):
        print("Say Parent")
        super(Parent, self).say()
        print("Said Parent")


class CalculatorBase(object):
    def calc(self):
        print("Calculator Base")


class ModelBase(CalculatorBase):
    def run(self):
        self.calc()


class ImprovedCalculator(object):
    def calc(self):
        print("Improved Calculator")


class ImprovedModel(ImprovedCalculator, ModelBase):
    """Really improved model.

    Note inheritance order.
    >>> ImprovedModel().run()
    Improved Calculator
    """
    pass


class NotSoImprovedModel(ModelBase, ImprovedCalculator):
    """Actually only base model.

    Note inheritance order here.
    >>> NotSoImprovedModel().run()
    Calculator Base
    """
    pass


class AltImprovedModel(ModelBase, ImprovedCalculator):
    """That doesnt work either.

    Same as NotSoImprovedModel, but tried to redefine run().
    >>> AltImprovedModel().run()
    Calculator Base
    """

    def run(self):
        self.calc()


if __name__ == '__main__':
    import doctest
    doctest.testmod()

import CWiPy.MembershipFunction as mf


class QuantifierSet:

    @staticmethod
    def almost_none() -> mf.MembershipFunction:
        almost_none = mf.TrapezoidMembershipFunction(0, 0, 0.05, 0.30)
        almost_none.name = 'almost none'
        return almost_none

    @staticmethod
    def few() -> mf.MembershipFunction:
        few = mf.TriangularMembershipFunction(0.05, 0.30, 0.50)
        few.name = 'few'
        return few

    @staticmethod
    def some() -> mf.MembershipFunction:
        some = mf.TriangularMembershipFunction(0.30, 0.50, 0.70)
        some.name = 'some'
        return some

    @staticmethod
    def many() -> mf.MembershipFunction:
        many = mf.TriangularMembershipFunction(0.50, 0.70, 0.90)
        many.name = 'many'
        return many

    @staticmethod
    def most() -> mf.MembershipFunction:
        most = mf.TrapezoidMembershipFunction(0.70, 0.90, 1, 1)
        most.name = 'most'
        return most

    @staticmethod
    def get_quantifiers():
        return [QuantifierSet.almost_none(), QuantifierSet.few(),
                QuantifierSet.some(), QuantifierSet.many(),
                QuantifierSet.most()]

    @staticmethod
    def dict_quantifiers():
        """

        Returns:
            dictionary of quantifier name and quantifier itself
        """
        result = {'almost_none': QuantifierSet.almost_none(),
                  'few': QuantifierSet.few(), 'some': QuantifierSet.some(),
                  'many': QuantifierSet.many(), 'most': QuantifierSet.most()}
        return result


class QuantifierSetOnParams:
    def __init__(self, min, max):
        """
        QuantifiersSet: defines the set of quantifiers such as almost_none,
        few, some, many and some
        :rtype:
        :param min: lower bound
        :param max: upper bound
        """
        self.min = min
        self.max = max

    def _point(self, percentage) -> float:
        return self.min + percentage * (self.max - self.min)

    def almost_none(self) -> mf.MembershipFunction:
        return mf.TrapezoidMembershipFunction(self.min, self.min,
                                              self._point(0.05),
                                              self._point(0.30))

    def few(self) -> mf.MembershipFunction:
        return mf.TriangularMembershipFunction(self._point(0.05),
                                               self._point(0.30),
                                               self._point(0.50))

    def some(self) -> mf.MembershipFunction:
        return mf.TriangularMembershipFunction(self._point(0.30),
                                               self._point(0.50),
                                               self._point(0.70))

    def many(self) -> mf.MembershipFunction:
        return mf.TriangularMembershipFunction(self._point(0.50),
                                               self._point(0.70),
                                               self._point(0.90))

    def most(self) -> mf.MembershipFunction:
        return mf.TrapezoidMembershipFunction(self._point(0.70),
                                              self._point(0.90), self.max,
                                              self.max)

    def get_quantifiers(self):
        return [self.almost_none(), self.few(), self.some(), self.many(),
                self.most()]

    def dict_quantifiers(self):
        result = {}
        result['almost_none'] = self.almost_none()
        result['few'] = self.few()
        result['some'] = self.some()
        result['many'] = self.many()
        result['most'] = self.most()
        return result

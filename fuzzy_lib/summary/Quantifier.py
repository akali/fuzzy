import fuzzy_lib.MembershipFunction as mf


class QuantifierSet:
    def __init__(self, min, max):
        """
        QuantifiersSet: defines the set of quantifiers such as almost_none, few, some, many and some
        :rtype:
        :param min: lower bound
        :param max: upper bound
        """
        self.min = min
        self.max = max

    def _point(self, percentage) -> float:
        return self.min + percentage * (self.max - self.min)

    def almost_none(self) -> mf.MembershipFunction:
        return mf.TrapezoidMembershipFunction(self.min, self.min, self._point(0.05), self._point(0.30))

    def few(self) -> mf.MembershipFunction:
        return mf.TriangularMembershipFunction(self._point(0.05), self._point(0.30), self._point(0.50))

    def some(self) -> mf.MembershipFunction:
        return mf.TriangularMembershipFunction(self._point(0.30), self._point(0.50), self._point(0.70))

    def many(self) -> mf.MembershipFunction:
        return mf.TriangularMembershipFunction(self._point(0.50), self._point(0.70), self._point(0.90))

    def most(self) -> mf.MembershipFunction:
        return mf.TrapezoidMembershipFunction(self._point(0.70), self._point(0.90), self.max, self.max)

    def get_quantifiers(self):
        return [self.almost_none(), self.few(), self.some(), self.many(), self.most()]

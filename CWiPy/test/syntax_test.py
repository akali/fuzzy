import unittest

from CWiPy.MembershipFunction import TrapezoidMembershipFunction, TriangularMembershipFunction
from CWiPy.Syntax import FuzzyQuery


class SyntaxTest(unittest.TestCase):
    def test_to_sql(self):
        query = "young age but very high salary"
        fields = {
            "age": {
                "young": TrapezoidMembershipFunction(10, 10, 18, 30),
                "middle": TriangularMembershipFunction(18, 30, 45),
                "old": TrapezoidMembershipFunction(30, 45, 100, 100),
            },
            "salary": {
                "low": TrapezoidMembershipFunction(0, 0, 20000, 50000),
                "middle": TrapezoidMembershipFunction(40000, 50000, 200000, 300000),
                "high": TrapezoidMembershipFunction(250000, 400000, 7000000, 7000000),
            },
        }

        print(FuzzyQuery(query, fields, alpha_cut=0.5, round_values=True).to_sql())


if __name__ == '__main__':
    unittest.main()

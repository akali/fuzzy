import unittest

from fuzzy.MembershipFunction import TrapezoidMembershipFunction, TriangularMembershipFunction
from fuzzy.Syntax import to_sql


class SyntaxTest(unittest.TestCase):
    def test_to_sql(self):
        query = "very very young age but very high salary"
        fields = {
            "age": {
                "young": TriangularMembershipFunction(10, 20, 30),
                "middle": TriangularMembershipFunction(25, 35, 45),
                "old": TriangularMembershipFunction(50, 100, 20000),
            },
            "salary": {
                "low": TrapezoidMembershipFunction(0, 0, 20000, 50000),
                "middle": TrapezoidMembershipFunction(40000, 50000, 200000, 300000),
                "high": TrapezoidMembershipFunction(250000, 400000, 7000000, 7000000),
            },
        }

        print(to_sql(query, fields))

        pass


if __name__ == '__main__':
    unittest.main()

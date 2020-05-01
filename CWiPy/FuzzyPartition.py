import CWiPy.MembershipFunction as mf


class FuzzyPartition:
    def __init__(self, start, end, points, aliases):
        self.start = start
        self.end = end
        self.points = points
        self.aliases = aliases

    def set_division(self, count):
        points = []
        step = float(self.end - self.start) / (count + 1)

        cur = self.start + step

        while cur < self.end:
            points.append(cur)
            cur += step

        self.points = points

    def get_membership_functions(self):
        result = {}
        start, end, points = self.start, self.end, self.points
        n = len(points)

        for i in range(n):
            if i == 0:
                cur = mf.TrapezoidMembershipFunction(start, start, points[0], points[1])
            elif i + 1 == n:
                cur = mf.TrapezoidMembershipFunction(points[i - 1], points[i], end, end)
            else:
                cur = mf.TriangularMembershipFunction(points[i - 1], points[i], points[i + 1])

            cur.name = self.aliases[i]

            result[self.aliases[i]] = cur

        return result

    def get_points(self):
        result = []
        start, end, points = self.start, self.end, self.points
        n = len(points)

        for i in range(n):
            if i == 0:
                cur = [{"x": start, "y": 1, "line_id": -1}, {"x": points[i], "y": 1, "line_id": i}]

                for j in range(i + 1, n):
                    cur.append({"x": points[j], "y": 0, "line_id": j}, )

                cur.append({"x": end, "y": 0, "line_id": n})
            elif i + 1 == n:
                cur = [{"x": start, "y": 0, "line_id": -1}]
                for j in range(i):
                    cur.append({"x": points[j], "y": 0, "line_id": j})
                cur.append({"x": points[i], "y": 1, "line_id": i})
                cur.append({"x": end, "y": 1, "line_id": n})
            else:
                cur = [{"x": start, "y": 0, "line_id": -1}]
                for j in range(i):
                    cur.append({"x": points[j], "y": 0, "line_id": j})
                cur.append({"x": points[i], "y": 1, "line_id": i})

                for j in range(i + 1, n):
                    cur.append({"x": points[j], "y": 0, "line_id": j})

                cur.append({"x": end, "y": 0, "line_id": n})

            result.append(cur)

        return result

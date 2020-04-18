class FuzzyPartition:
    def __init__(self, start, end, points, aliases):
        self.start = start
        self.end = end
        self.points = points
        self.aliases = aliases

    def getPoints(self):
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

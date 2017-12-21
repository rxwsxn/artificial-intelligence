
class ValueItr(object):

    def __init__(self):
        self.U = {}
        self.U_p = {}
        self.S = []

    def __initialize(self):
        for i in range(7):
            for j in range(7):
                self.U[i, j] = 0.0
                self.U_p[i, j] = 0.0
                self.S.append((i, j))

    def __maximize(self, s, wind_case):
        A = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
        maximum = -100000
        for a in A:
            s_p = (a[0] + s[0], a[1] + s[1])
            if 1 <= wind_case <= 3 and s[1] in range(3, 6):
                s_p = (s_p[0] - wind_case + 1, s_p[1])
            if s_p[0] > 6:
                s_p = (6, s_p[1])
            if s_p[0] < 0:
                s_p = (0, s_p[1])
            if s_p[1] > 6:
                s_p = (s_p[0], 6)
            if s_p[1] < 0:
                s_p = (s_p[0], 0)
            pr = self.U[s_p]
            maximum = max(maximum, pr)

        return maximum

    def __reward(self, s):
        if s[0] == 3 and s[1] == 6:
            return 0.0
        else:
            return -1.0

    def __pr(self, s_p, s, a):
        s_a = (a[0] + s[0], a[1] + s[1])
        if s_p == s_a:
            return 1
        else:
            return 0

    def __print_U(self):
        string = ""
        for i in range(7):
            for j in range(7):
                string += str("%.1f" % self.U_p[i, j]) + " \t"
            string += "\n"
        print(string)

    def value_iteration(self, max_iters, discount, e, wind_case):
        self.__initialize()
        iters = 0
        while iters < max_iters:
            iters += 1
            self.U = self.U_p
            d = 0
            for s in self.S:
                self.U_p[s] = self.__reward(s) + discount * self.__maximize(s, wind_case=wind_case)
                if abs(self.U_p[s] - self.U[s]) > d:
                    d = abs(self.U_p[s] - self.U[s])
                    if d < 0.001:
                        break
        self.__print_U()


if __name__ == '__main__':
    MAX_ITERS = 1000
    e = 0.001
    y = 1
    v = ValueItr()
    for i in range(1, 4):
        v.value_iteration(max_iters=MAX_ITERS, discount=y, e=e, wind_case=i)

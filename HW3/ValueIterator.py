
def print_string(U):
    res = ""
    for i in range(7):
        for j in range(7):
            res += str('%.1f' % U[(i,j)]) +" " +"\t"
        res += "\n"
    print res

def actionResultList(U_prime, (i,j), windCase):
    res = []
    stay = [i,j]
    N = [i-1, j]
    NE = [i-1, j+1]
    E = [i, j + 1]
    SE = [i + 1, j + 1]
    S = [i + 1, j]
    SW = [i + 1, j - 1]
    W = [i, j - 1]
    NW = [i - 1, j - 1]
    for a in [stay, N, NE, E, SE, S, SW, W, NW]:
        # deduction of row according to wind
        if j == 3 or j == 4 or j == 5:
            a[0] -= windCase - 1
        # x index boundary check
        if a[0] > 6:
            a[0] = 6
        if a[0] < 0:
            a[0] = 0           
        # y index boundary check
        if a[1] > 6:
            a[1] = 6
        if a[1] < 0:
            a[1] = 0         
        res.append([tuple(a), U_prime[tuple(a)]])
    return res

def findMax(U, L):
    # print L
    maximum = float('-inf')
    for i in range(len(L)):
        maximum = max(maximum, U[L[i][0]] * L[i][1])
    return maximum

def main():
    U_prime = {}
    R = {}
    S = []
    MAX_ITERS = 1000
    sigma = 0.001
    gamma = 1
    
    for i in range(7):
        for j in range(7):
            U_prime[(i, j)] = 0.0
            S.append((i, j))
            R[(i, j)] = -1.0
            if i == 3 and j == 6:
                R[(i, j)] = 0.0
    # print "S:", S   
    # print "R:", R
    print "===CS4710 Value Iterator Shell==="
    windCase = int(raw_input("What is your wind case in 1, 2, or 3?\n-> "))
    print "Initial U\'"
    print_string(U_prime)
    
    for iter in range(MAX_ITERS):
        U = {}
        for key in U_prime:
            U[key] = U_prime[key]
        delta = 0
        
        for s in S:
            U_prime[s] = R[s] + gamma * findMax(U, actionResultList(U_prime, s, windCase))
            # print "-->", U_prime[s], U[s]
            delta = max(delta, abs(U_prime[s] - U[s]))
                
        print "Iteration:", iter
        print delta
        print_string(U_prime)
        if (delta < sigma):
            break

    print "U\' after Value Iteration with wind case", windCase
    print_string(U_prime)

    return 0

if __name__ == "__main__":
    main()
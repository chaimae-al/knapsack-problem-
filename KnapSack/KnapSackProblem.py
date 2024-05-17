import random
import time

# global variables
N = 5
v = [4, 2, 1, 10, 2]
w = [12, 2, 1, 4, 1]
x = [0,0,0,0,0] 
xMin =[0,0,0,0,0] 
maxIterations = 5

# objective function
def f():
    res = 0
    for i in range(N):
        res += (v[i] * x[i])
    return res

# weight function
def weight():
    res = 0
    for i in range(N):
        res += w[i] * x[i]
    return res

# weight constraint function
def c1():
    d = weight()
    if (d <= 15):
        return True
    return False

# display functions
def afficherX():
    print("The solution is : [", end='')
    for i in range(N):
        print(x[i], end=' ')
    print("]", end=' ')

def afficherV():
    print("The values are : [", end='')
    for i in range(N):
        print(v[i], end=' ')
    print("]", end=' ')

def afficherW():
    print("The weights are : [", end='')
    for i in range(N):
        print(w[i], end=' ')
    print("] ", end='')

def randomSolution():
    for i in range(N):
        x[i] = (random.randint(0, 1))

def randomAlgorithm():
    k = 0
    fmin = f()
    while (k < maxIterations):
        randomSolution()
        
        if ((f() > fmin) and (c1() == True)):
            fmin = f()
            for i in range(N):
                xMin[i] = x[i]
            randomSolution()
        k += 1
        for i in range(N):
            x[i] = xMin[i]
        
        
        print("\nIteration " + str(k) + ": ", end='')
        afficherX()
        print(" ")
        afficherW()
        print(" w = ", end=' ')
        print(f(), end=' ')
        afficherV()
        print(" v = ", end=' ')
        print(weight(), end='')
    


if __name__ == "__main__":
    randomAlgorithm()
    print("\nWe are using " + str(maxIterations) + " iterations")
    afficherV()
    print(" ")
    afficherW()
    t1 = time.time()
    # print("\n")
    randomAlgorithm()
    print("\n-------------------Please wait------------------")
    print("\nsolution optimale : ")
    afficherX()
    print(" ",end=' ')
    afficherW()
    print(" w = ", end=' ')
    print(f(), end=' ')
    afficherV()
    print(" v = ", end=' ')
    print(weight())
    t2 = time.time()
    print("Total execution time : " + str(t2 - t1) + " seconds", end=' ')

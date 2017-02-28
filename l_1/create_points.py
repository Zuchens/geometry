import random
import math
import csv
import matplotlib.pyplot as plt

def PointsInCircum(r,n=20):
    return [(math.cos(2*math.pi/n*x)*r,math.sin(2*math.pi/n*x)*r) for x in xrange(0,n+1)]

def lines(n):
    X = [random.uniform(-1000, 1000) for i in range(0,n)]
    return[(x,0.05*x+0.05) for x in X]

f = open("100_points.csv","w+")
X = []
Y= []
for i in range(0,100000):
    first_num = random.uniform(-100,100)
    second_num = random.uniform(-100,100)
    f.write(str(first_num) + ";"+str(second_num)+"\n")
    X.append(first_num)
    Y.append(second_num)
plt.scatter(X,Y)
# plt.show()

f = open("10_14_points.csv","w+")
X = []
Y= []
for i in range(0,100000):
    first_num = '{0:.14f}'.format(random.uniform(-100000000000000,100000000000000))
    second_num = '{0:.14f}'.format(random.uniform(-100000000000000,100000000000000))
    f.write(str(first_num) + ";"+str(second_num)+"\n")
    X.append(first_num)
    Y.append(second_num)
plt.scatter(X,Y)
# plt.show()



X = []
Y= []
points = PointsInCircum(100,1000)
with open("circle.csv","w+") as out:
    csv_out = csv.writer(out,delimiter=";")
    for row in points:
        csv_out.writerow(row)
        X.append(row[0])
        Y.append(row[1])

plt.scatter(X,Y)
# plt.show()


X = []
Y = []
points = lines(1000)
with open("line.csv", "w+") as out:
    csv_out = csv.writer(out, delimiter=";")
    for row in points:
        csv_out.writerow(row)
        X.append(row[0])
        Y.append(row[1])

plt.scatter(X, Y)
# plt.show()
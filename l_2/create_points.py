import random
import math
import csv
import matplotlib.pyplot as plt

def PointsInCircum(r,n=20):
    return [(math.cos(2*math.pi/n*x)*r,math.sin(2*math.pi/n*x)*r) for x in xrange(0,n+1)]

def lines(n):
    X = [random.uniform(-1000, 1000) for i in range(0,n)]
    return[(x,0.05*x+0.05) for x in X]

def segments_X(n, start,end,Y):
    X = [random.uniform(start, end) for i in range(0,n)]
    return [(x,Y) for x in X]

def segments_Y(n, start,end,X):
    Y = [random.uniform(start, end) for i in range(0,n)]
    return [(X,y) for y in Y]

def segments_XY(n, start,end):
    Y = [random.uniform(start, end) for i in range(0,n)]
    return [(y,y) for y in Y]

def minus_segments_XY(n, start,end):
    Y = [random.uniform(start, end) for i in range(0,n)]
    return [(y,end-y) for y in Y]

def create_points_on_sqr(n):
    segments = []
    for i in range(0,n):
        x = random.randint(0,3)
        if x == 0: segment = segments_X(1,-10,10,10)
        if x == 1: segment = segments_X(1,-10,10,-10)
        if x == 2: segment = segments_Y(1,-10,10,10)
        if x == 3: segment = segments_Y(1,-10,10,-10)
        segments.append(segment[0])
    return segments

    plt.scatter([x[0]for x in segments], [x[1]for x in segments])
    plt.show()
def create_points_sqr():
    X =[(0,10),(0,0),(10,0),(10,10)]
    X.extend(segments_X(25, 0, 10, 0))
    X.extend(segments_Y(25, 0, 10, 0))
    X.extend(segments_XY(25, 0, 10))
    X.extend(minus_segments_XY(25, 0, 10))

    return X

    # plt.scatter([x[0]for x in X], [x[1]for x in X])
    # plt.show()
##f = open("100_points.csv","w+")
def create_points(n,start,end):
    X = []
    Y= []
    for i in range(0,n):
       first_num = random.uniform(start,end)
       second_num = random.uniform(start,end)
       X.append(first_num)
       Y.append(second_num)
    return [(x,y) for x,y in zip(X,Y)]

# X = create_points(100,-100,100)
# #
# X = create_points_sqr()
# plt.scatter([x[0] for x in X], [x[1] for x in X])
# plt.show()
#plt.scatter(X,Y)
##plt.savefig('100_points.png')
##
##f = open("10_14_points.csv","w+")
##X = []
##Y= []
##for i in range(0,100000):
##    first_num = '{0:.14f}'.format(random.uniform(-100000000000000,100000000000000))
##    second_num = '{0:.14f}'.format(random.uniform(-100000000000000,100000000000000))
##    f.write(str(first_num) + ";"+str(second_num)+"\n")
##    X.append(first_num)
##    Y.append(second_num)
##plt.scatter(X,Y)
##plt.savefig('10_14_points.png')
##
##
##
##X = []
##Y= []
##points = PointsInCircum(100,1000)
##with open("circle.csv","w+") as out:
##    csv_out = csv.writer(out,delimiter=";")
##    for row in points:
##        csv_out.writerow(row)
##        X.append(row[0])
##        Y.append(row[1])
##print points
##plt.scatter(X,Y)
##plt.savefig('circle.png')


# X = []
# Y = []
# points = lines(1000)
# with open("line.csv", "w+") as out:
#     csv_out = csv.writer(out, delimiter=";")
#     for row in points:
#         csv_out.writerow(row)
#         X.append(row[0])
#         Y.append(row[1])

# plt.scatter(X, Y)
# plt.show()
##plt.savefig('line.png')

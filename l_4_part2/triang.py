import copy
import json
import math

import operator
from matplotlib import pyplot as plt

from l_4.go_gui import *

MAX = 100
class Point():

    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        return "Point id:%d x:%f y:%f chain:%s" %(self.id, self.x, self.y, self.chain)
    def __repr__(self):
        return "Point id:%d x:%.2f y:%.2f chain:%s" %(self.id, self.x, self.y,self.chain)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x,self.y))

class Line ():
    def __init__(self,a,b,id = 0,helper = None):
        self.id = id
        self.begin = a
        self.end = b

    def __str__(self):
        return "Line id:%d Begin x:%f y:%f End: x:%f y:%f\n" % (self.id, self.begin.x, self.begin.y, self.end.x, self.end.y)


    def __repr__(self):
        return "Line id:%d Begin x:%f y:%f End: x:%f y:%f\n" % (self.id, self.begin.x, self.begin.y, self.end.x, self.end.y)


class LineBuilder:
    def __init__(self, line):
        self.line = line
        self.xs = list()
        self.ys = list()
        self.points = []
        self.id_p = 0
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        if event.inaxes!=self.line.axes: return
        self.xs.append(event.xdata)
        self.ys.append(event.ydata)
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()
        p = Point(self.id_p,event.xdata,event.ydata)
        self.points.append(p)
        self.id_p+=1

    def __repr__(self):
        return "line"


def angles(x1, y1, x2, y2):
    numer = (x1 * x2 + y1 * y2)
    denom = math.sqrt((x1 ** 2 + y1 ** 2) * (x2 ** 2 + y2 ** 2))
    return math.acos(numer / denom)


def cross_sign(x1, y1, x2, y2):
    return x1 * y2 > x2 * y1

def has_ang(p1,ref,p2):

    x1, y1 = p1.x - ref.x, p1.y - ref.y
    x2, y2 = p2.x - ref.x, p2.y - ref.y
    angle = angles(x1, y1, x2, y2)
    if cross_sign(x1, y1, x2, y2):
        angle = 2*math.pi - angle
    if p1.y > ref.y and p2.y > ref.y and angle > math.pi: #laczac
        return 0
    elif p1.y < ref.y and p2.y < ref.y and angle > math.pi: #dziel
        return 1
    elif p1.y < ref.y and p2.y < ref.y and angle < math.pi: #pocz
        return 2
    elif p1.y > ref.y and p2.y > ref.y and angle < math.pi: #konc
        return 3
    else:
        return 4 #praw
    return True

def is_inside(p1,ref,p2):
    x1, y1 = p1.x - ref.x, p1.y - ref.y
    x2, y2 = p2.x - ref.x, p2.y - ref.y
    # print('Points', p1, ref, p2)
    if cross_sign(x1, y1, x2, y2):
        return True
    else:
        return False
def obj_dict(obj):
    return obj.__dict__
def plot_line(p1,p2):
    plt.plot((p1.x, p2.x), (p1.y, p2.y), 'black')
def plot_point(p1,color):
    colors = ["yellow", "cyan","red","green", "black"]
    plt.scatter(p1.x,p1.y,c=colors[color], s = 150 )
is_monotone = True
class Helper():
    def __init__(self,el,v = None):
        self.el = el
        self.v =v
def ccw(A, B, C):
    return (B.x - A.x) * (C.y - A.y) < (B.y - A.y) * (C.x - A.x)

def helper_point(vl,p,vp):
    return  [x for x in points if not ccw(vl,p,x) and ccw(vp,p,x) and x.y >p.y][-1]
def cross(a, b):
    c = a[0] * b[1] - b[0] * a[1]
    return c

def intersect(l1,l2):
    p = [l1.begin.x,l1.begin.y]
    p_r = [l1.end.x ,l1.end.y]
    r =  map(operator.sub,p_r ,p)
    q = [l2.begin.x,l2.begin.y]
    q_s = [l2.end.x ,l2.end.y]
    s = map(operator.sub,q_s , q)
    if cross(r,s)!=0:
        t = cross(map(operator.sub,q , p), s )/ cross(r , s)
        u = cross(map(operator.sub,q , p), r) / cross(r , s)
        if t>=0 and t<=1 and u>=0 and u<=1:
            point = map(operator.add,p,[t*r1 for r1 in r])
            return point
    return 0

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click to build line segments')
line, = ax.plot([0], [0])
plt.xlim((0,100))
plt.ylim((0,100))
linebuilder = LineBuilder(line)

plt.show()
points =  linebuilder.points
lines = []
for i in range(0,len(points)-1):
    l = Line(i,points[i],points[i+1])
    lines.append(l)
lines.append(Line(i+1,points[len(points)-1],points[0]))

# a0 = Point(0,5.0,10.0)
# a1 = Point(1,5.0,6.0)
# a2 = Point(2,4.2,4.5)
# a3 = Point(3,2.0,4.0)
# a4 = Point(4,4.0,3.0)
# a5 = Point(5,0.0,2.0)
# a6 = Point(6,10.0,1.0)
# a7 = Point(7,6.0,9.0)
# points = [a0,a1,a2,a3,a4,a5,a6,a7]
#
# a0 = Point(0,3.0,10.0)
# a1 = Point(1,3.0,9.0)
# a2 = Point(2,0.2,8.4)
# a3 = Point(3,3.0,7.2)
# a4 = Point(4,0.0,6.0)
# a5 = Point(5,3.0,5.0)
# a6 = Point(6,0.0,4.0)
# a7 = Point(7,3.0,3.0)
# a8 = Point(8,16.0,0.0)
# points = [a0,a1,a2,a3,a4,a5,a6,a7,a8]
p = []
ls = []
lines = []
jlines = []
for ids in range(0,len(points)):
    color = has_ang(points[(ids-1)%len(points)],points[(ids)%len(points)],points[(ids+1)%len(points)])
    plot_line(points[(ids-1)%len(points)],points[(ids)%len(points)])
    pl = points[ids]
    pl.color = color
    p.append(pl)
    lines.append(Line(points[(ids) % len(points)], points[(ids + 1) % len(points)]))
    jlines.append(JsonLine(points[(ids) % len(points)], points[(ids + 1) % len(points)]))
    ls.append([points[(ids-1)%len(points)],points[(ids)%len(points)],points[(ids+1)%len(points)]])
    plot_point(points[(ids)%len(points)],color)

is_monotone = True
for ids in range(0,len(points)-2):
    if not has_ang(points[(ids-1)],points[ids+1],points[ids+2]):
        is_monotone = False
if not has_ang(points[len(points)-2], points[len(points)-1], points[0]):
    is_monotone = False
if not has_ang(points[len(points) - 1], points[0], points[len(points)-1]):
    is_monotone = False
print is_monotone
max_point = max(points, key = lambda p: p.y)
min_point = min(points, key = lambda p: p.y)

while True:
    if points[0] == max_point:
        break
    else:
        point = points.pop(0)
        points.append(point)

end_left_chain = False

for x in points:
    if x == min_point:
        end_left_chain = True
    if end_left_chain == False:
        x.chain = "left"
    else:
        x.chain = "right"
max_point.chain = "middle"

min_point.chain = "middle"
Q = sorted(points, key=lambda p: p.y, reverse=True)
history = []
# Q = points
stack = [Q.pop(0),Q.pop(0)]
j_l =  copy.copy(jlines)
triang = []
while Q:
    x = Q.pop(0)
    print "Stack" +  str(stack)
    if stack[-1].chain!= x.chain:
        # print "Compare" + str(stack[-1]) + " " +  str(x)
        points_his = [PointHistory(p.id, "normal") for p in set(points) - set(list([stack[-1], x]))]
        points_his.extend([PointHistory(p.id, "active") for p in set(list([stack[-1], x]))])
        lines_his = [LineHistory(line_id, "normal") for line_id in range(0, len(jlines))]
        history.append(HistoryPeriod(copy.copy(points_his), copy.copy(lines_his)))

        for i in stack:
            print "Different chains", i
            plt.plot((i.x, x.x), (i.y, x.y), 'blue')
            if x!= i and x!=stack[-1] and stack[-1]!=i:
                triang.append((i,x,stack[-1]))
            line = JsonLine(i, x)
            points_his = [PointHistory(p.id, "normal") for p in set(points)-set(list([stack[-1],i,x]))]
            points_his.extend([PointHistory(p.id, "active") for p in set(list([stack[-1],i,x]))])
            lines_his = [LineHistory(line_id, "normal") for line_id in range(0, len(jlines))]
            jlines.append(line)
            lines_his.append(LineHistory(jlines.index(line), "active"))
            history.append(HistoryPeriod(copy.copy(points_his), copy.copy(lines_his)))

        stack.append(x)
        stack=stack[-2:]
    else:
        while len(stack) >= 2 and is_inside(x, stack[-1], stack[-2]):
            print "is_inside", x
            # print "Compare" + str(stack[-2]) + " " + str(stack[-1]) + " " + str(x)
            plt.plot((stack[-2].x, x.x), (stack[-2].y, x.y), 'blue')
            if x!= stack[-2] and x!=stack[-1] and stack[-1]!= stack[-2]:
                triang.append((x,stack[-2],stack[-1]))
            line = JsonLine(stack[-2], x)

            points_his = [PointHistory(p.id, "normal") for p in set(points)-set(list([x, stack[-1], stack[-2]]))]
            points_his.extend([PointHistory(p.id, "active") for p in set(list([x, stack[-1], stack[-2]]))])
            lines_his = [LineHistory(line_id, "normal") for line_id in range(0, len(jlines))]
            jlines.append(line)
            lines_his.append(LineHistory(jlines.index(line), "active"))
            history.append(HistoryPeriod(copy.copy(points_his), copy.copy(lines_his)))

            # if len(stack) >= 2:
            stack.pop(-1)
            stack.append(x)
            # else:
            #     break

        if len(stack) > 1:
            if not is_inside(x, stack[-1], stack[-2]):
                print "is_outside", x
                points_his = [PointHistory(p.id, "normal") for p in set(points) - set(list([x, stack[-1], stack[-2]]))]
                points_his.extend([PointHistory(p.id, "active") for p in set(list([x, stack[-1], stack[-2]]))])
                lines_his = [LineHistory(line_id, "normal") for line_id in range(0, len(jlines))]
                history.append(HistoryPeriod(copy.copy(points_his), copy.copy(lines_his)))

                stack.append(x)

jsonS = [JsonPoint(x.x, -x.y) for x in points]


points_his = [PointHistory(x.id, "normal") for x in points]
lines_his = [LineHistory(x, "normal") for x in range(0,len(j_l))]
lines_his.extend([LineHistory(l, "active") for l in range(len(j_l),len(jlines))])
history.append(HistoryPeriod(copy.copy(points_his), copy.copy(lines_his)))
his = json.dumps(GoGuiJson(jsonS,jlines,history), default=obj_dict)
# print his

print len(triang)
plt.show()

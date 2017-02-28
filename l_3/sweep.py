import json
import operator
import random
from copy import copy

from go_gui import PointHistory, JsonPoint, HistoryPeriod, GoGuiJson, LineHistory, JsonLine


class Point():

    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        return "Point id:%d x:%f y:%f \n" %(self.id, self.x, self.y)
    def __repr__(self):
        return "Point id:%d x:%.2f y:%.2f\n" %(self.id, self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x,self.y))

class Line ():
    def __init__(self,id,a,b):
        self.id = id
        if a.x<b.x:
            self.begin = a
            self.end = b
        else:
            self.begin = b
            self.end = a
    def __str__(self):
        return "Line id:%d Begin x:%f y:%f End: x:%f y:%f\n" % (self.id, self.begin.x, self.begin.y,self.end.x, self.end.y)
    def __repr__(self):
        return "Line id:%d Begin x:%f y:%f End: x:%f y:%f\n" % (self.id, self.begin.x, self.begin.y,self.end.x, self.end.y)

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

def obj_dict(obj):
    return obj.__dict__

def remove_duplicates(values):
    output = []
    seen = set()
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output
#

def pop_random(lst):
    idx = random.randrange(0, len(lst))
    return lst.pop(idx)

def height(line,x):
    return (line.end.y - line.begin.y)*(x - line.begin.x)/(line.end.x -  line.begin.x) + line.begin.y

S1 = [Point(x,round(random.uniform(0,10),3),round(random.uniform(0,15),3)) for x in range(0,20)]
S2 = copy(S1)
pairs = []
line_id =0
lines = []
#
# while S2:
#     rand1 = pop_random(S2)
#     rand2 = pop_random(S2)
#     pair = JsonLine(rand1, rand2)
#     lines.append(Line(line_id,rand1, rand2))
#     line_id+=1
#     pairs.append(pair)


a0 = Point(0,0.0,1)
a1 = Point(1,4.0,2)
b0 = Point(2,4.0,0)
b1 = Point(3,6.0,1)
c0 = Point(4,2.0,3)
c1 = Point(5,6.0,0.5)
d0 = Point(6,1.0,6)
d1 = Point(7,2.0,2)
e0 = Point(8,0.0,8)
e1 = Point(9,7.0,-1)
S1 = [a0,a1,b0,b1,c0,c1,d0,d1,e0,e1]
pairs = [JsonLine(a0,a1),JsonLine(b0,b1),JsonLine(c0,c1),JsonLine(d0,d1),JsonLine(e0,e1)]
lines = [Line(0,a0,a1),Line(1,b0,b1),Line(2,c0,c1),Line(3,d0,d1),Line(4,e0,e1)]
line_id = 5
S = sorted(S1, key=lambda x: (x.x, x.y), reverse = False)

T = []
Q = S
history = []


points = [PointHistory(x.id, "normal") for x in Q]
lines_his = [LineHistory(x, "normal") for x, val in enumerate(pairs)]
history.append(HistoryPeriod(copy(points), copy(lines_his)))
point_id  =len(S1)
intersect_points = set()
broom_lines = []

dict = {}
while Q != []:
    print T
    p = Q.pop(0)

    broom_top = Point(point_id, p.x, max([x.y for x in S])+4)
    point_id+=1
    broom_bottom = Point(point_id, p.x, min([x.y for x in S])-4)
    point_id+=1
    broom_lines.append(Line(line_id,broom_top,broom_bottom))
    bottom_top = [Line(line_id,broom_top,broom_bottom)]
    line_id+=1
    S1.append(broom_bottom)
    S1.append(broom_top)
    pairs.append(JsonLine(broom_top,broom_bottom))
    points = [PointHistory(x.id, "normal") for x in set(S1)-set([p])]
    points.append(PointHistory(p.id, "active") )
    broom_lines_his =  [LineHistory(x.id, "active") for x in bottom_top]
    broom_lines_his.extend([LineHistory(x.id, "normal") for x in set(lines)])
    history.append(HistoryPeriod(copy(points), copy(broom_lines_his)))


    at_start =  next((x for x in lines if x.begin == p),[])
    if at_start:
        T.append(at_start)

        points = [PointHistory(x.id, "normal") for x in set(S1)-set([p])]
        points.append(PointHistory(p.id, "active"))
        lines_his = [LineHistory(x.id, "normal") for x in set(lines)-set(T)]
        lines_his.extend([LineHistory(x.id, "active") for x in T])
        lines_his.extend( [LineHistory(x.id, "active") for x in bottom_top])
        history.append(HistoryPeriod(copy(points), copy(lines_his)))

    at_end = next((x for x in lines if x.end == p),[])
    if at_end:
        T.remove(at_end)

        points = [PointHistory(x.id, "normal") for x in set(S1)-set([p])]
        points.append(PointHistory(p.id, "active"))
        lines_his = [LineHistory(x.id, "normal") for x in set(lines)-set(T)]
        lines_his.extend([LineHistory(x.id, "active") for x in T])
        lines_his.extend( [LineHistory(x.id, "active") for x in bottom_top])
        history.append(HistoryPeriod(copy(points), copy(lines_his)))
    #
    if  p in dict:
        # print p
        s = dict[p][0]
        s1 = dict[p][1]
        a,b = T.index(s),T.index(s1)
        T[b], T[a] = T[a], T[b]
    for s in range(0,len(T)-1):
        # for s1 in T:
            if T[s]!=T[s+1]:
                # print T[s], T[s+1]
                point =intersect(T[s],T[s+1])
                if point !=0 and point[0]>p.x:
                    i_point = Point(point_id, point[0], point[1])
                    if i_point not in dict:
                        dict[i_point]=[T[s],T[s+1]]

                        point_id+=1
                        intersect_points.add(i_point)
                        points = [PointHistory(x.id, "normal") for x in S1]
                        points.append(PointHistory(i_point.id, "active"))
                        lines_his = [LineHistory(x.id, "normal") for x in set(lines) - set(T)]
                        lines_his.extend([LineHistory(x.id, "active") for x in T])
                        history.append(HistoryPeriod(copy(points), copy(lines_his)))
                        Q.append(i_point)
                        S1.append(i_point)
    T = sorted(T,key=lambda h: height(h,p.x), reverse = True)
    Q = remove_duplicates(Q)
    Q = sorted(Q, key=lambda x: (x.x, x.y), reverse=False)



S2 = S1
# history.append(HistoryPeriod(copy(points), copy(lines_his)))
jsonS = [JsonPoint(x.x,-x.y)for x in S2]
his = json.dumps(GoGuiJson(jsonS,pairs,history), default=obj_dict)
f = open("points.json","w+")
f.write(his)

# print intersect_points




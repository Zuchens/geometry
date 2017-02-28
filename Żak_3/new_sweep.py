import json
import operator
import random
from copy import copy

from go_gui import PointHistory, JsonPoint, HistoryPeriod, GoGuiJson, LineHistory, JsonLine
from l_3.BST import *


class Point():

    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        return "Point id:%d (%f,%f) \n" %(self.id, self.x, self.y)
    def __repr__(self):
        return "Point id:%d (%f,%f) \n" %(self.id, self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x #and self.y == other.y
    def __lt__(self, other):
        return self.x < other.x #and self.y == other.y

    def __hash__(self):
        return hash((self.x,self.y))

class Line ():
    def __init__(self,id,a,b):
        self.id = id
        if a.x<=b.x:
            self.begin = a
            self.end = b
        else:
            self.begin = b
            self.end = a
        if a.x == b.x:
            self.begin.x+=0.01

    def __str__(self):
        return "Line id:%d Begin x:%f y:%f End: x:%f y:%f" % (self.id, self.begin.x, self.begin.y,self.end.x, self.end.y)
    def __repr__(self):
        return "Line id:%d Begin x:%f y:%f End: x:%f y:%f" % (self.id, self.begin.x, self.begin.y,self.end.x, self.end.y)


    def __lt__(self, other):
        if self.begin.x > other.begin.x:
            p_x = other.begin.x
            y1 = height(self, p_x)
            return y1 < other.begin.y
        else:
            p_x = self.begin.x
            y2 = height(other, p_x)
            return y2 > other.begin.y  # and self.y == other.y

    def __le__(self, other):
        if self.begin.x > other.begin.x:
            p_x = other.begin.x
            y1 = height(self, p_x)
            return y1 < other.begin.y
        else:
            p_x = self.begin.x
            y2 = height(other, p_x)
            return y2 > other.begin.y  # and self.y == other.y
    # def __eq__(self, other):
    #     return self.id == other.id  # and self.y == other.y


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
    if (line.end.x -  line.begin.x) !=0:
        return (line.end.y - line.begin.y)*(x - line.begin.x)/(line.end.x -  line.begin.x) + line.begin.y
    else:
        return (line.end.y - line.begin.y)*(x - line.begin.x)/(line.end.x-  line.begin.x) + line.begin.y

def sweep(BSTtype=BST):
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


    a0 = Point(0,1.0,5)
    a1 = Point(1,10.18,1.48)
    b0 = Point(2,1.94,3.14)
    b1 = Point(3,2.8,3.52)
    c0 = Point(4,2.42,2.22)
    c1 = Point(5,3.2,2.68)
    d0 = Point(6,2.0,1)
    d1 = Point(7,9.84,5.16)
    e0 = Point(8,7.58,6.04)
    e1 = Point(9,6.6,1.24)
    f0 = Point(10,8.36,5.96)
    f1 = Point(11,7.62,1.4)
    g0 = Point(12,6.28,1.62)
    g1 = Point(13,4.95,0.98)
    h0 = Point(14,1.5,-1.62)
    h1 = Point(15,1.54,7.98)
    i0 = Point(16,8.44,0.52)
    j0 = Point(17,1.86,7.48)
    j1 = Point(18,4.5,7.48)

    S1 = [a0,a1,b0,b1,c0,c1,d0,d1,e0,e1,f0,f1,g0,g1,h0,h1,i0,j0,j1]
    for i in range(0,len(S1)-2):
        for j in range(i+1,len(S1)-1):
            if S1[i].x==S1[j].x:
                S1[i].x+=0.001


    pairs = [JsonLine(a0,a1),JsonLine(b0,b1),JsonLine(c0,c1),JsonLine(d0,d1),JsonLine(e0,e1),JsonLine(f0,f1),JsonLine(g0,g1),JsonLine(h0,h1),JsonLine(i0,a1),JsonLine(j1,j0)]
    lines = [Line(0,a0,a1),Line(1,b0,b1),Line(2,c0,c1),Line(3,d0,d1),Line(4,e0,e1),Line(5,f0,f1),Line(6,g0,g1),Line(7,h0,h1),Line(8,i0,a1),Line(9,j1,j0)]

    line_id = 10
    S = sorted(S1, key=lambda x: (x.x, x.y), reverse = False)
    pairs2 = copy(pairs)
    T = []
    Q = S
    mytree = BSTtype()
    for x in Q:
        mytree.insert(x)
    history = []

    Ttree = BSTtype()
    points = [PointHistory(x.id, "normal") for x in Q]
    lines_his = [LineHistory(x, "normal") for x, val in enumerate(pairs)]
    history.append(HistoryPeriod(copy(points), copy(lines_his)))
    point_id  =len(S1)
    intersect_points = set()
    broom_lines = []

    dict = {}



    while mytree.root!=None:
        # print "Ttree"
        # print Ttree
        p = mytree.minimum()
        mytree.delete(p)
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

        at_start =  [x for x in lines if x.begin == p]
        if len(at_start) == 1:
            T.append(at_start[0])
            Ttree.insert(at_start[0])
            points = [PointHistory(x.id, "normal") for x in set(S1)-set([p])]
            points.append(PointHistory(p.id, "active"))
            lines_his = [LineHistory(x.id, "normal") for x in set(lines)-set(T)]
            lines_his.extend([LineHistory(x.id, "active") for x in T])
            lines_his.extend( [LineHistory(x.id, "active") for x in bottom_top])
            history.append(HistoryPeriod(copy(points), copy(lines_his)))

        if len(at_start)>1:
            for begin in at_start:
                T.append([begin])
                intersect_points.add(p)
                Ttree.insert(begin)
        # at_end = next((x for x in lines if x.end == p),[])
        at_end =  [x for x in lines if x.end == p]
        if len(at_end) ==1:
            T.remove(at_end[0])
            Ttree.delete(at_end[0])
            points = [PointHistory(x.id, "normal") for x in set(S1)-set([p])]
            points.append(PointHistory(p.id, "active"))
            lines_his = [LineHistory(x.id, "normal") for x in set(lines)-set(T)]
            lines_his.extend([LineHistory(x.id, "active") for x in T])
            lines_his.extend( [LineHistory(x.id, "active") for x in bottom_top])
            history.append(HistoryPeriod(copy(points), copy(lines_his)))
        if len(at_end)>1:
            for ends in at_end:
                T.remove(ends)
                Ttree.delete(ends)
                intersect_points.add(p)
        #
        if  p in dict:
            s = dict[p][0]
            s1 = dict[p][1]
            a,b = T.index(s),T.index(s1)
            T[b], T[a] = T[a], T[b]
            s1.p = p
            s.p = p
            # Ttree.swap(s,s1,T)
        list_T  = Ttree.makeList(Ttree.root)
        T = list_T[::-1]
        for s in range(0,len(T)-1):
                if T[s]!=T[s+1]:
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
                            mytree.insert(i_point)
                            S1.append(i_point)
        T = sorted(T,key=lambda h: height(h,p.x), reverse = True)


    S2 = S1

    points = [PointHistory(x.id, "normal") for x in S2]
    points.extend([PointHistory(x.id, "active") for x in intersect_points ])
    lines_his = [LineHistory(x, "normal") for x, val in enumerate(pairs2)]
    history.append(HistoryPeriod(copy(points), copy(lines_his)))
    # history.append(HistoryPeriod(copy(points), copy(lines_his)))
    jsonS = [JsonPoint(x.x,-x.y)for x in S2]
    his = json.dumps(GoGuiJson(jsonS,pairs,history), default=obj_dict)
    f = open("points.json","w+")
    f.write(his)

    print intersect_points
sweep()
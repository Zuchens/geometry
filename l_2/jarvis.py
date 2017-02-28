import copy
import json
import random
import time
start_time = time.time()
from create_points import  PointsInCircum, create_points_sqr, create_points_on_sqr



from go_gui import *


def obj_dict(obj):
    return obj.__dict__

def ccw(A, B, C):
    res =  (C.y-A.y)*(B.x-A.x) - (B.y-A.y)*(C.x-A.x)
    return res

class Point():

    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y

a = Point(0,0.0,-10.0)
b = Point(1,3.0,4.0)
c = Point(2,2.0,5.0)
d = Point(3,1.0,6.0)
e = Point(4,0.01,6.0)
f = Point(5,3.0,2.0)
# S = [a,b,c,d,e,f]#,a1,b1]#,c1,d1,e1,f1]
S = create_points_on_sqr(2000)
# S = create_points_sqr()
# S = PointsInCircum(20,100)
S  = [Point(x, s[0],s[1]) for x,s in enumerate(S)]
# S = [Point(x,random.uniform(0,50),random.uniform(0,50)) for x in range(0,2000)]

jsonS = [JsonPoint(x.x,-x.y)for x in S]
hull = []

history = []
lines = []
j=0


sorted_list = sorted(S, key=lambda p: (p.x,p.y))
p0 = sorted_list[0]

p,q,l=0,0,0
lines = []
lines_his = []
breakpoint = 40
condition = True
while condition :
    hull.append(sorted_list[p])
    points = [PointHistory(x.id, "active") for x in hull]
    points.extend([PointHistory(x.id, "normal") for x in set(sorted_list)-set(hull)])
    if len(hull)>1:
        lines.append(JsonLine(hull[-2], hull[-1]))
        lines_his.append(LineHistory(j, "normal"))
        j = j+1
    q=(p+1)%len(S)
    for i in range(0,len(sorted_list)):
        if p!=i and ccw(sorted_list[p],sorted_list[i],sorted_list[q])>0:
            lines.append(JsonLine(sorted_list[p], sorted_list[q]))
            all_lines = copy.copy(lines_his)
            all_lines.append(LineHistory(j, "normal"))
            history.append(HistoryPeriod(copy.copy(points), all_lines))
            j = j + 1
            q=i
    p=q
    breakpoint=breakpoint-1
    history.append(HistoryPeriod(copy.copy(points), copy.copy(lines_his)))#
    condition = p != l# and breakpoint > 0

points = [PointHistory(x.id, "active") for x in hull]
points.extend([PointHistory(x.id, "normal") for x in set(sorted_list) - set(hull)])
lines.append(JsonLine(hull[0], hull[-1]))
lines_his.append(LineHistory(j, "normal"))
history.append(HistoryPeriod(copy.copy(points), copy.copy(lines_his)))
# his = json.dumps(GoGuiJson(jsonS,lines,history), default=obj_dict)
# d = open('points.json', 'w+')
# d.write(his)
print("--- %s seconds ---" % (time.time() - start_time))
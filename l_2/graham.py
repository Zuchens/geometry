import copy
import json
import operator

import math
import random

from create_points import *
from create_points import create_points_sqr
from go_gui import *
import time
start_time = time.time()

def ccw(A, B, C):
    res =  (C.y-A.y)*(B.x-A.x) - (B.y-A.y)*(C.x-A.x)
    return res

def remove_duplicates(seq):
    new_list = [seq[-1]]
    last = seq[-1]
    for x in reversed(seq):
        if(last.angle != x.angle):
            last = x
            new_list.append(x)
    return new_list



class Point():

    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y

    def add_angle(self,p0):
        self.angle = (self.y -p0.y)/(self.x - p0.x) if self.x - p0.x !=0 else float('inf')
        # ax = (self.x - p0.x)
        # ay = (self.y - p0.y)
        # self.angle = ax/math.sqrt(ax**2+ay**2)
        return self


def obj_dict(obj):
    return obj.__dict__

a = Point(0,0.0,-10.0)
b = Point(1,3.0,4.0)
c = Point(2,2.0,5.0)
d = Point(3,1.0,6.0)
e = Point(4,0.01,6.0)
f = Point(5,3.0,2.0)

a1 = Point(6,0.04,-10.02)
b1 = Point(7,13.0,43.0)
# c1 = Point(8,2.0,15.0)
# d1 = Point(9,11.0,6.0)
# e1 = Point(10,0.31,6.0)
# f1 = Point(11,3.4,12.0)
# S = [a,b,c,d,e,f,a1,b1]#,c1,d1,e1,f1]
X = create_points_on_sqr(2000)
# X = create_points_sqr()
# X = PointsInCircum(20,600)
# S = [Point(x,random.uniform(0,50),random.uniform(0,50)) for x in range(0,2000)]
S = [Point(x,val[0],val[1]) for x,val in enumerate(X)]
jsonS = [JsonPoint(x.x,-x.y)for x in S]
#
# json_string = json.dumps(jsonS, default=obj_dict)
# all_points = []
# history = []
# for x in range(0,len(S)):
#     all_points.append(PointHistory(x,"active"))
#     his_points = HistoryPeriod(copy.copy(all_points), [])
#     history.append(his_points)
#
#
# his = json.dumps(GoGuiJson(jsonS,[],history), default=obj_dict)
# print his
#
history = []
lines = []

i=1
S = sorted(S, key=lambda p: p.y)
sorted_list = sorted(S, key=lambda p: p.x)

p0 = sorted_list.pop(0)
angles_list = sorted([x.add_angle(p0) for x in sorted_list], key=lambda p: p.angle, reverse=True)#,math.sqrt(p.x*p.x + p.y*p.y)))
angles_list = remove_duplicates(angles_list)


p1 = angles_list.pop(0)
p2 = angles_list.pop(0)
stack = [p0,p1 ,p2]

lines.append(JsonLine(stack[0],stack[1]))
lines.append(JsonLine(stack[1],stack[2]))
points = [PointHistory(x.id,"active")for x in stack]
lines_his =[LineHistory(i-1,"normal"),LineHistory(i,"active")]
history.append(HistoryPeriod(copy.copy(points), copy.copy(lines_his)))

not_in_stack = []
while angles_list:
    lines_his = [LineHistory(x.lineID, "normal") for x in lines_his]
    while ccw(stack[-3],stack[-2],stack[-1]) <0:
        if ccw(stack[-3],stack[-2],stack[-1]) > 0:
            pass
        else:
            i = i + 1
            not_in_stack.append(stack.pop(-2))
            lines_his = [LineHistory(x.lineID, "normal") for x in lines_his]
            lines_his.pop()
            lines_his.pop()
            lines.append(JsonLine(stack[-1], stack[-2]))
            lines_his.append(LineHistory(i, "active"))
            points = [PointHistory(x.id, "active") for x in stack[:-1]]
            points.append(PointHistory(stack[-1].id, "active"))
            points.extend([PointHistory(x.id, "normal") for x in not_in_stack])
            history.append(HistoryPeriod(copy.copy(points), copy.copy(lines_his)))
    in_loop =  False
    while ccw(stack[-2],stack[-1],angles_list[0])==0:
        if angles_list:
            stack[-1] = angles_list.pop(0)
            in_loop = True
    if in_loop:
        i = i + 1
        lines_his = [LineHistory(x.lineID, "normal") for x in lines_his]
        lines.append(JsonLine(stack[-1], stack[-2]))
        lines_his.append(LineHistory(i, "active"))
        points = [PointHistory(x.id, "normal") for x in stack[:-1]]
        points.append(PointHistory(stack[-1].id, "active"))
        points.extend([PointHistory(x.id, "normal") for x in not_in_stack])
        history.append(HistoryPeriod(copy.copy(points), copy.copy(lines_his)))
    i = i+1
    stack.append(angles_list.pop(0))
    lines_his = [LineHistory(x.lineID, "normal") for x in lines_his]
    lines.append(JsonLine(stack[-1], stack[-2]))
    lines_his.append(LineHistory(i, "active"))
    points = [PointHistory(x.id, "normal") for x in stack[:-1]]
    points.append(PointHistory(stack[-1].id,"active"))
    points.extend([PointHistory(x.id, "normal") for x in not_in_stack])
    history.append(HistoryPeriod(copy.copy(points), copy.copy(lines_his)))

if ccw(stack[-3], stack[-2], stack[-1])>0:
    i = i + 1
    lines_his = [LineHistory(x.lineID, "normal") for x in lines_his]
    lines.append(JsonLine(stack[0], stack[-1]))
    lines_his.append(LineHistory(i, "active"))
    points = [PointHistory(x.id, "normal") for x in sorted_list]
else:
    i = i + 1
    not_in_stack.append(stack.pop(-2))
    lines_his = [LineHistory(x.lineID, "normal") for x in lines_his]
    lines_his.pop()
    lines_his.pop()
    lines.append(JsonLine(stack[-1], stack[-2]))
    lines_his.append(LineHistory(i, "active"))
    points = [PointHistory(x.id, "active") for x in stack[:-1]]
    points.append(PointHistory(stack[-1].id, "active"))
    points.extend([PointHistory(x.id, "normal") for x in not_in_stack])
    history.append(HistoryPeriod(copy.copy(points), copy.copy(lines_his)))
    i = i + 1
    lines_his = [LineHistory(x.lineID, "normal") for x in lines_his]
    lines.append(JsonLine(stack[0], stack[-1]))
    lines_his.append(LineHistory(i, "active"))
    points = [PointHistory(x.id, "normal") for x in set(S)]

history.append(HistoryPeriod(copy.copy(points), copy.copy(lines_his)))
print("END")

# his = json.dumps(GoGuiJson(jsonS,lines,history), default=obj_dict)
# print his

print("--- %s seconds ---" % (time.time() - start_time))
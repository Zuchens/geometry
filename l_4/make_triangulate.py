import math

import operator
from matplotlib import pyplot as plt

MAX = 100
class Point():

    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y

    def __str__(self):
        return "\nPoint id:%d x:%f y:%f \n" %(self.id, self.x, self.y)
    def __repr__(self):
        return "\nPoint id:%d x:%.2f y:%.2f\n" %(self.id, self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x,self.y))

class Line ():
    def __init__(self,a,b,id = 0,helper = None):
        self.id = id
        self.begin = a
        self.end = b
        self.helper = helper


    def __str__(self):
        return "Line id:%d Begin x:%f y:%f End: x:%f y:%f\n" % (self.id, self.begin.x, self.begin.y, self.end.x, self.end.y)


    def __repr__(self):
        return "Line id:%d Begin x:%f y:%f End: x:%f y:%f\n" % (self.id, self.begin.x, self.begin.y, self.end.x, self.end.y)


class LineBuilder:
    def __init__(self, line):
        self.line = line
        # self.xs = list(line.get_xdata())
        # self.ys = list(line.get_ydata())
        self.xs = list()
        self.ys = list()
        self.points = []
        self.id_p = 0
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        # print('click', self.xs, self.ys)
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



fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('click to build line segments')
line, = ax.plot([0], [0])  # empty line
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


def angles(x1, y1, x2, y2):
    # Use dotproduct to find angle between vectors
    # This always returns an angle between 0, pi
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
            # plt.scatter(point[0], point[1], s=90)
            return point
    return 0

p = []
ls = []
lines = []
for ids in range(0,len(points)):
    color = has_ang(points[(ids-1)%len(points)],points[(ids)%len(points)],points[(ids+1)%len(points)])
    plot_line(points[(ids-1)%len(points)],points[(ids)%len(points)])
    pl = points[ids]
    pl.color = color
    p.append(pl)
    lines.append(Line(points[(ids) % len(points)], points[(ids + 1) % len(points)]))

    ls.append([points[(ids-1)%len(points)],points[(ids)%len(points)],points[(ids+1)%len(points)]])
    # plot_line(points[ids+1], points[ids + 2])
    plot_point(points[(ids)%len(points)],color)


# plt.plot((-MAX, MAX), (MAX, MAX), 'red')
Q = sorted(ls, key=lambda p: p[1].y, reverse=True)
points = [x[1] for x in ls]
points = sorted(points, key=lambda p: p.y, reverse=True)

# print Q
# print lines
T = []
# while Q!= []:
#     l = Q.pop(0)
#     # print l[0].color, l[1].color, l[2].color
#     k = Line(Point(0,-MAX,l[1].y),Point(0,MAX,l[1].y))
#     plt.plot((-MAX,MAX), (l[1].y,l[1].y), 'red')
#     p = l[1]
#     vl = l[0]
#     vp = l[2]
#     current_lines = [x for x in lines if (x.begin.y>=p.y and x.end.y <=p.y) or (x.begin.y<=p.y and x.end.y >=p.y)]
#     # wielokat jest po prawej
#
#     current_lines = [(x,intersect(k,x)) for x in current_lines]
#     current_lines = sorted(current_lines, key = lambda p : p[1][0])
#     if p.color ==0:#laczacy
#         evp = [x[0] for x in current_lines if x[1][0]>p.x+0.2][0]
#         # plt.plot((evp.begin.x, evp.end.x), (evp.begin.y, evp.end.y), 'blue')
#         vi = [x for x in points if intersect(Line(p,vp), k)[0] < x.x and intersect(evp, k)[0] > x.x][-1]
#         # plt.scatter(vi.x, vi.y, c = 'black', s=90)
#         # plt.scatter(p.x, p.y, c = 'black', s=90)
#         if vi.color ==0:
#             line = (p, vi)
#             plt.plot((p.x, vi.x), (p.y, vi.y), 'blue')
#             # T.remove(evp)
#         # ev = [x for x in T if intersect(k,x)][-1]
#         ev = [x[0] for x in current_lines if x[1][0]+0.2<p.x][-1]
#         vi = [x for x in points if intersect(ev, k)[0] < x.x and intersect(Line(vl,p), k)[0] > x.x][-1]
#         # plt.plot((p.x, vi.x), (p.y, vi.y), 'blue')
#         if vi.color ==0:
#             line = (p, vi)
#             plt.plot((p.x, vi.x), (p.y, vi.y), 'blue')
#             ev.helper = vi
#     if p.color == 1:#dziel
#         ev = [x for x in T if intersect(k,x)][0] # or -1
#         evp = [x[0] for x in current_lines if x[1][0]>p.x+0.2][0]
#         vi = [x for x in points if intersect(ev,k)[0]<x.x and intersect(evp,k)[0] > x.x][0]
#         line = (p,vi)
#         plt.plot((p.x,vi.x), (p.y, vi.y), 'blue')
#         ev.helper = vi
#         evp.helper = vi
#         T.append(evp)
#         # point = helper_point(ev[0], ev[1], vp)
#     if p.color == 2:#pocz
#         T.append(Line(vp,p,p))
#         plt.plot((vp.x, p.x), (vp.y, p.y), 'red')
#     if p.color == 3:#konc
#         if helper_point(vl,p,vp).color == 0:
#             line = (p,helper_point(vl,p,vp))
#             plt.plot((p.x, helper_point(vl,p,vp).x), (p.y, helper_point(vl,p,vp).y), 'blue')
#         # T.remove((p,vl))
#
#             # T.append(())
#     if p.color == 4:#reg
#         if l[0].y>l[2].y:
#             vg = l[0]
#             vd = l[2]
#         else:
#             vg = l[2]
#             vd = l[0]

        # x1, y1 = vg.x - p.x, vg.y - p.y
        # x2, y2 = vd.x - p.x, vd.y - p.y
        # angle = angles(x1, y1, x2, y2)
        # if cross_sign(x1, y1, x2, y2):
        #     if



# color = has_ang(points[len(points)-2], points[len(points)-1], points[0])
# plot_line(points[len(points)-2], points[len(points)-1])
# plot_line(points[len(points)-1], points[0])
# plot_point(points[len(points)-1], color)
# color = has_ang(points[len(points) - 1], points[0], points[1])
# plot_point(points[0], color)



plt.show()
print is_monotone

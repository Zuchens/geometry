import math
from matplotlib import pyplot as plt


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
        self.begin = a
        self.end = b


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
    if p1.y > ref.y and p2.y > ref.y and angle > math.pi:
        return False
    if p1.y < ref.y and p2.y < ref.y and angle > math.pi:
        return False
    return True


is_monotone = True
for ids in range(0,len(points)-2):
    if not has_ang(points[(ids-1)],points[ids+1],points[ids+2]):
        is_monotone = False
if not has_ang(points[len(points)-2], points[len(points)-1], points[0]):
    is_monotone = False
if not has_ang(points[len(points) - 1], points[0], points[len(points)-1]):
    is_monotone = False
print is_monotone

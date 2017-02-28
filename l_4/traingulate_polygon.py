import json
import math
from matplotlib import pyplot as plt

from go_gui import JsonPoint


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

def IsConvex(a, b, c):
	# only convex if traversing anti-clockwise!
	crossp = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
	if crossp >= 0:
		return True
	return False

def InTriangle(a, b, c, p):
	L = [0, 0, 0]
	eps = 0.0000001
	# calculate barycentric coefficients for point p
    # eps is needed as error correction since for very small distances denom->0
	L[0] = ((b[1] - c[1]) * (p[0] - c[0]) + (c[0] - b[0]) * (p[1] - c[1])) \
		  /(((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])) + eps)
	L[1] = ((c[1] - a[1]) * (p[0] - c[0]) + (a[0] - c[0]) * (p[1] - c[1])) \
		  /(((b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])) + eps)
	L[2] = 1 - L[0] - L[1]
	# check if p lies in triangle (a, b, c)
	for x in L:
		if x >= 1 or x <= 0:
			return False
	return True

def IsClockwise(poly):
	# initialize sum with last element
	sum = (poly[0][0] - poly[len(poly)-1][0]) * (poly[0][1] + poly[len(poly)-1][1])
	# iterate over all other elements (0 to n-1)
	for i in range(len(poly)-1):
		sum += (poly[i+1][0] - poly[i][0]) * (poly[i+1][1] + poly[i][1])
	if sum > 0:
		return True
	return False

def GetEar(poly):
	size = len(poly)
	if size < 3:
		return []
	if size == 3:
		tri = (poly[0], poly[1], poly[2])
		del poly[:]
		return tri
	for i in range(size):
		tritest = False
		p1 = poly[(i-1) % size]
		p2 = poly[i % size]
		p3 = poly[(i+1) % size]
		if IsConvex(p1, p2, p3):
			for x in poly:
				if not (x in (p1, p2, p3)) and InTriangle(p1, p2, p3, x):
					tritest = True
			if tritest == False:
				del poly[i % size]
				return (p1, p2, p3)
	print('GetEar(): no ear found')
	return []



tri = []
plist = linebuilder.points
plist = [(p.x,p.y) for p in plist]
while len(plist) >= 3:
    a = GetEar(plist)
    if a == []:
        break
    tri.append(a)

print tri

# jsonS = [JsonPoint(x.x,-x.y)for x in points]
# his = json.dumps(GoGuiJson(jsonS,pairs,history), default=obj_dict)
# f = open("points.json","w+")
# f.write(his)
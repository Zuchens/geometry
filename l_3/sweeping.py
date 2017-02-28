from __future__ import division

# Thanks to @Kris for the intersection algorithm in python
# http://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
import random

from go_gui import JsonPoint
from go_gui import PointHistory


class Point():

    def __init__(self,id,x,y):
        self.id = id
        self.x = x
        self.y = y


def find_intersection( p0, p1, p2, p3 ) :

    s10_x = p1[0] - p0[0]
    s10_y = p1[1] - p0[1]
    s32_x = p3[0] - p2[0]
    s32_y = p3[1] - p2[1]

    denom = s10_x * s32_y - s32_x * s10_y

    if denom == 0 : return None # collinear

    denom_is_positive = denom > 0

    s02_x = p0[0] - p2[0]
    s02_y = p0[1] - p2[1]

    s_numer = s10_x * s02_y - s10_y * s02_x

    if (s_numer < 0) == denom_is_positive : return None # no collision

    t_numer = s32_x * s02_y - s32_y * s02_x

    if (t_numer < 0) == denom_is_positive : return None # no collision

    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive : return None # no collision


    # collision detected

    t = t_numer / denom

    intersection_point = [ p0[0] + (t * s10_x), p0[1] + (t * s10_y) ]
    return intersection_point

S = [Point(x,random.uniform(0,50),random.uniform(0,50)) for x in range(0,60)]
jsonS = [JsonPoint(x.x,-x.y)for x in S]
line_segments = [[(1,4), (4,4)], [(2,3), (5,3)], [(3,2), (6,2)], [(6.5, 1), (7,1)], [(7.5, 0), (8.5,0)]]
# red lines
test_segments = [[(4.5,0), (4.5,4.5)], [(6.25, 0), (6.25, 4.5)]]

# Check all lines for intersections
intersections = set()

points = [PointHistory(x.id, "normal") for x in S]



for test_segment in test_segments:
    for line_segment in line_segments:
        print test_segment, line_segment
        p0, p1 = test_segment[0], test_segment[1]
        p2, p3 = line_segment[0], line_segment[1]
        result = find_intersection(p0, p1, p2, p3)
        if result is not None:
            intersections.add(tuple(result))

print intersections


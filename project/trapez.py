from project.binary_tree import Tree

v1 = (5.0, 9.0)
v2 = (2.0, 7.0)
v3 = (7.0, 8.0)
v4 = (4.0, 6.0)
v5 = (7.0, 5.0)
v6 = (4.0, 4.5)
v7 = (1.0, 4.0)
v8 = (6.0, 2.0)
v9 = (3.0, 0.0)

e1 = (v1, v2)
e2 = (v1, v3)
e3 = (v1, v4)
e4 = (v3, v4)
e5 = (v5, v3)
e6 = (v4, v5)
e7 = (v4, v6)
e8 = (v7, v2)
e9 = (v7, v4)
e10 = (v7, v6)
e11 = (v5, v6)
e12 = (v8, v5)
e13 = (v9, v8)
e14 = (v9, v5)
e15 = (v9, v6)
e16 = (v9, v7)

MAX = 100
tree = Tree()

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return str(self.p1) + "  " +str(self.p2)


def divide_graph(V, E, idx):
    V1 = V[:idx]
    V2 = V[idx:]
    E1 = [x for x in E if x.p1 in V1 or x.p2 in V1]
    E2 = [x for x in E if x.p1 in V2 or x.p2 in V2]
    return [(V1, E1), (V2, E2)]


def get_median_idx(V):
    return len(V) / 2


def crossing_edges(last_k,k,V,E):
    cross_edges = []
    if k!= None and last_k!=None:
        for edge in E:
            if edge.p1[1] > k.p1[1] and edge.p2[1] <last_k.p1[1]:
                cross_edges.append(edge)
    return cross_edges

def split_plane(V, E, cross_edges):
    pass


def cut_segment(e, last_k, k):
    #sort wrong_x
    new_x1 = ((e.p2[0] - e.p1[0])*(k.p1[1] - e.p1[1]))/(e.p2[1]-e.p1[1]) +  e.p1[0]
    new_x2 = ((e.p2[0] - e.p1[0])*(last_k.p1[1] - e.p1[1]))/(e.p2[1]-e.p1[1]) + e.p1[0]
    line = Line((new_x1,k.p1[1]),(new_x2,last_k.p1[1]))
    return line


def trapezoid(V, E, last_k = None, last_node = None):
    median_idx = get_median_idx(V)
    divided = divide_graph(V,E,median_idx)
    k = Line((-MAX,V[median_idx][1]), (MAX,V[median_idx][1]))
    tree.add(k)
    print k
    for g in divided:
        print g[0]
        cross_edges = crossing_edges(last_k,k,g[0],g[1])
        if cross_edges:
            new_segments = []
            for e in cross_edges:
                segment = cut_segment(e,last_k,k)
                new_segments.append(segment)
            T = split_plane(g[0],g[1],cross_edges)
            for i in bst:
                if i:
                    trapezoid(i,k,bluenode)
                else:
                    tree.add_leaf()
        else:
            trapezoid(g[0],g[1],k,k)



V = [v1, v2, v3, v4, v5, v6, v7, v8, v9]
E = [e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14, e15, e16]
E2 = [Line(e[0],e[1]) for e in E]

V = sorted(V, reverse=True, key=lambda p: p[1])

E2 = sorted(E2, key=lambda p: p.p1[0])

D = sorted(V,key = lambda p: p[1])
trapezoid(V,E2)
print tree
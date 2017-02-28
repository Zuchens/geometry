class GoGuiJson():
    def __init__(self, points, lines, history):
        self.points = points
        self.lines = lines
        self.history = history


class JsonPoint():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class JsonLine():
    def __init__(self, p1, p2):
        self.p1 = p1.id
        self.p2 = p2.id


class HistoryPeriod():
    def __init__(self, point_history, lines_history):
        self.points = point_history
        self.lines = lines_history


class PointHistory():
    def __init__(self, point_id, style):
        self.pointID = point_id
        self.style = style


class LineHistory():
    def __init__(self, line_id, style):
        self.lineID = line_id
        self.style = style

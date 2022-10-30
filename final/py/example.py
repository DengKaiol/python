import random
from copy import deepcopy

import pisqpipe as pp
from pisqpipe import DEBUG_EVAL, DEBUG

pp.infotext = 'name="pbrain-pyrandom", author="Jan Stransky", version="1.0", country="Czech Republic", www="https://github.com/stranskyjan/pbrain-pyrandom"'

MAX_BOARD = 20
board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
max_depth = 1


def brain_init():
    if pp.width < 5 or pp.height < 5:
        pp.pipeOut("ERROR size of the board")
        return
    if pp.width > MAX_BOARD or pp.height > MAX_BOARD:
        pp.pipeOut("ERROR Maximal board size is {}".format(MAX_BOARD))
        return
    pp.pipeOut("OK")


def brain_restart():
    for x in range(pp.width):
        for y in range(pp.height):
            board[x][y] = 0
    pp.pipeOut("OK")


def isFree(x, y):
    return x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] == 0


def brain_my(x, y):
    if isFree(x, y):
        board[x][y] = 1
    else:
        pp.pipeOut("ERROR my move [{},{}]".format(x, y))


def brain_opponents(x, y):
    if isFree(x, y):
        board[x][y] = 2
    else:
        pp.pipeOut("ERROR opponents's move [{},{}]".format(x, y))


def brain_block(x, y):
    if isFree(x, y):
        board[x][y] = 3
    else:
        pp.pipeOut("ERROR winning move [{},{}]".format(x, y))


def brain_takeback(x, y):
    if x >= 0 and y >= 0 and x < pp.width and y < pp.height and board[x][y] != 0:
        board[x][y] = 0
        return 0
    return 2


class Node:
    def __init__(self, state):
        self.state = state
        self.value = None
        self.coordinate = None


# 返回效用值
def utility_my(node):
    value = 0
    boardstate = node.state
    coordinates = coordinates_sequence(node.coordinate)
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=4, color=True):
        value += 100000
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=3, color=True):
        value += 10000
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=2, color=True):
        value += 1000
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=1, color=True):
        value += 200
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=4, color=False):
        value += 80000
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=3, color=False):
        value += 60000
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=2, color=False):
        value += 500
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=1, color=False):
        value += 100
    return value


def utility_opponents(node):
    value = 0
    boardstate = node.state
    coordinates = coordinates_sequence(node.coordinate)
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=4, color=False):
        value += -100000
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=3, color=False):
        value += -10000
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=2, color=False):
        value += -1000
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=1, color=False):
        value += -200
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=4, color=True):
        value += -80000
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=3, color=True):
        value += -60000
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=2, color=True):
        value += -500
    if eight_coordinate_structure(state=boardstate, coordinates_sequence=coordinates, num=1, color=True):
        value += -100
    return value


def eight_coordinate_structure(state, coordinates_sequence, num, color):
    flag = 0
    number = 0
    for coordinates in coordinates_sequence:
        number += coordinate_structure(state=state, coordinates=coordinates, color=color)
        flag += 1
        if flag == 2:
            if number >= num:
                return True
            flag = 0
            number = 0
    return False


# 返回一个坐标周边的重要位置
def coordinates_sequence(coordinate):
    x, y = coordinate[0], coordinate[1]
    # 横竖斜
    coordinates, coordinates_sequence = [], []
    for i in range(1, 5, 1):
        if x - i >= 0:
            coordinates.append((x - i, y))
    coordinates_sequence.append(deepcopy(coordinates))
    coordinates.clear()
    for i in range(1, 5, 1):
        if x + i < MAX_BOARD:
            coordinates.append((x + i, y))
    coordinates_sequence.append(deepcopy(coordinates))
    coordinates.clear()
    for i in range(1, 5, 1):
        if y - i >= 0:
            coordinates.append((x, y - i))
    coordinates_sequence.append(deepcopy(coordinates))
    coordinates.clear()
    for i in range(1, 5, 1):
        if y + i < MAX_BOARD:
            coordinates.append((x, y + i))
    coordinates_sequence.append(deepcopy(coordinates))
    coordinates.clear()
    for i in range(1, 5, 1):
        if x - i >= 0 and y - i >= 0:
            coordinates.append((x - i, y - i))
    coordinates_sequence.append(deepcopy(coordinates))
    coordinates.clear()
    for i in range(1, 5, 1):
        if x + i < MAX_BOARD and y + i < MAX_BOARD:
            coordinates.append((x + i, y + i))
    coordinates_sequence.append(deepcopy(coordinates))
    coordinates.clear()
    for i in range(1, 5, 1):
        if x - i >= 0 and y + i < MAX_BOARD:
            coordinates.append((x - i, y + i))
    coordinates_sequence.append(deepcopy(coordinates))
    coordinates.clear()
    for i in range(1, 5, 1):
        if x + i < MAX_BOARD and y - i >= 0:
            coordinates.append((x + i, y - i))
    coordinates_sequence.append(deepcopy(coordinates))
    coordinates.clear()
    return coordinates_sequence


# 判定连子数
def coordinate_structure(state, coordinates, color):
    number = 0
    if color:
        for coordinate in coordinates:
            x, y = coordinate[0], coordinate[1]
            if state[x][y] == 1:
                number += 1
            elif state[x][y] == 0:
                if number == 3:
                    number += 1
                break
            elif state[x][y] == 2:
                if number == 3:
                    number -= 1
                break
        return number
    else:
        for coordinate in coordinates:
            x, y = coordinate[0], coordinate[1]
            if state[x][y] == 2:
                number += 1
            elif state[x][y] == 0:
                if number == 3:
                    number += 1
                break
            elif state[x][y] == 1:
                if number == 3:
                    number -= 1
                break
        return number


# 得到可能的后继坐标
def actions(node):
    keycoordinates = []
    emptycoordinates = []
    coordinates = []
    boardstate = deepcopy(node.state)
    for i in range(MAX_BOARD):
        for j in range(MAX_BOARD):
            if boardstate[i][j] != 0:
                keycoordinates.append((i, j))
            else:
                emptycoordinates.append((i, j))
    for empty in emptycoordinates:
        for key in keycoordinates:
            if abs(empty[0] - key[0]) < 4 and abs(empty[1] - key[1]) < 4:
                coordinates.append(empty)
                break
    if len(coordinates) == 0:
        coordinates.append((10, 10))
    return coordinates


# 得到后继节点
def result_my(node, action):
    successor = deepcopy(node)
    x, y = action[0], action[1]
    successor.state[x][y] = 1
    successor.coordinate = action
    return successor


# def result_my_max(node):
#     board_state = node.state
#     current_coordinate = node.coordinate
#     coordinates = actions(node=node)
#     all_successors = []
#     successors = []
#     value = 0
#     i_successor = None
#     if board_state[current_coordinate[0]][current_coordinate[1]] == 2:
#         for coordinate in coordinates:
#             successor = result_my(node=node, action=coordinate)
#             successor.value = utility_my(node=successor)
#             all_successors.append(successor)
#         for i in range(5):
#             for successor in all_successors:
#                 if successor.value > value:
#                     i_successor = successor
#             successors.append(i_successor)
#             all_successors.remove(i_successor)
#         return successors
#     else:
#         for coordinate in coordinates:
#             successor = result_opponents(node=node, action=coordinate)
#             successor.value = utility_opponents(node=successor)
#             all_successors.append(successor)
#         for i in range(5):
#             for successor in all_successors:
#                 if successor.value < value:
#                     i_successor = successor
#             successors.append(i_successor)
#             all_successors.remove(i_successor)
#         return successors


def result_opponents(node, action):
    successor = deepcopy(node)
    x, y = action[0], action[1]
    successor.state[x][y] = 2
    successor.coordinate = action
    return successor


# 最大深度检测
def terminal_test(depth):
    return depth >= max_depth


# 剪枝
def get_value_coordinate(node, alpha, beta):
    value, coordinate = max_value(node=node, alpha=alpha, beta=beta, depth=0)
    return coordinate


def max_value(node, alpha, beta, depth):
    if terminal_test(depth=depth):
        value = utility_opponents(node=node)
        coordinate = node.coordinate
        return value, coordinate
    value = float('-inf')
    coordinate = None
    current_node = deepcopy(node)
    coordinates = actions(node=current_node)
    for a in coordinates:
        successor = result_my(current_node, a)
        successor_value, successor_coordinate = min_value(node=successor, alpha=alpha, beta=beta, depth=depth + 1)
        if successor_value > value:
            value = successor_value
            coordinate = a
        if value >= beta:
            return value, coordinate
        alpha = max(alpha, value)
    return value, coordinate
    # successors = result_my_max(node=current_node)
    # for successor in successors:
    #     successor_value, successor_coordinate = min_value(node=successor, alpha=alpha, beta=beta, depth=depth + 1)
    #     if successor_value > value:
    #         value = successor_value
    #         coordinate = successor.coordinate
    #     if value >= beta:
    #         return value, coordinate
    #     alpha = max(alpha, value)
    # return value, coordinate


def min_value(node, alpha, beta, depth):
    if terminal_test(depth=depth):
        value = utility_my(node=node)
        coordinate = node.coordinate
        return value, coordinate
    value = float('inf')
    coordinate = None
    current_node = deepcopy(node)
    coordinates = actions(node=current_node)
    for a in coordinates:
        successor = result_opponents(current_node, a)
        successor_value, successor_coordinate = max_value(node=successor, alpha=alpha, beta=beta, depth=depth + 1)
        if successor_value < value:
            value = successor_value
            coordinate = a
        if value <= alpha:
            return value, coordinate
        beta = min(beta, value)
    return value, coordinate
    # successors = result_my_max(node=current_node)
    # for successor in successors:
    #     successor_value, successor_coordinate = max_value(node=successor, alpha=alpha, beta=beta, depth=depth + 1)
    #     if successor_value < value:
    #         value = successor_value
    #         coordinate = successor.coordinate
    #     if value <= alpha:
    #         return value, coordinate
    #     beta = min(beta, value)
    # return value, coordinate


def brain_turn():
    if pp.terminateAI:
        return
    current_board = board
    node = Node(state=current_board)
    coordinate = get_value_coordinate(node=node, alpha=float('-inf'), beta=float('inf'))
    x, y = coordinate[0], coordinate[1]
    pp.do_mymove(x, y)


def brain_end():
    pass


def brain_about():
    pp.pipeOut(pp.infotext)


if DEBUG_EVAL:
    import win32gui


    def brain_eval(x, y):
        # TODO check if it works as expected
        wnd = win32gui.GetForegroundWindow()
        dc = win32gui.GetDC(wnd)
        rc = win32gui.GetClientRect(wnd)
        c = str(board[x][y])
        win32gui.ExtTextOut(dc, rc[2] - 15, 3, 0, None, c, ())
        win32gui.ReleaseDC(wnd, dc)

######################################################################
# A possible way how to debug brains.
# To test it, just "uncomment" it (delete enclosing """)
######################################################################

# # define a file for logging ...
# DEBUG_LOGFILE = "D:\\f\py\py.log"
# # ...and clear it initially
# with open(DEBUG_LOGFILE, "w") as f:
#     pass
#
#
# # define a function for writing messages to the file
# def logDebug(msg):
#     with open(DEBUG_LOGFILE, "a") as f:
#         f.write(msg + "\n")
#         f.flush()
#
#
# # define a function to get exception traceback
# def logTraceBack():
#     import traceback
#     with open(DEBUG_LOGFILE, "a") as f:
#         traceback.print_exc(file=f)
#         f.flush()
#     raise
#
#
# # use logDebug wherever
# # use try-except (with logTraceBack in except branch) to get exception info
# # an example of problematic function
# def brain_turn():
#     logDebug("some message 1")
#     try:
#         logDebug("some message 2")
#         1. / 0.  # some code raising an exception
#         logDebug("some message 3")  # not logged, as it is after error
#     except:
#         logTraceBack()
#

######################################################################

# "overwrites" functions in pisqpipe module
pp.brain_init = brain_init
pp.brain_restart = brain_restart
pp.brain_my = brain_my
pp.brain_opponents = brain_opponents
pp.brain_block = brain_block
pp.brain_takeback = brain_takeback
pp.brain_turn = brain_turn
pp.brain_end = brain_end
pp.brain_about = brain_about
if DEBUG_EVAL:
    pp.brain_eval = brain_eval


def main():
    pp.main()


if __name__ == "__main__":
    main()

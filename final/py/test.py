# import example
#
# MAX_BOARD = 20
# board = [[0 for i in range(MAX_BOARD)] for j in range(MAX_BOARD)]
# max_depth = 1
#
# board[17][17] = 2
# node = example.Node(state=board)
#
#
# def brain_turn():
#     current_board = board
#     node = example.Node(state=current_board)
#     coordinate = example.get_value_coordinate(node=node, alpha=float('-inf'), beta=float('inf'))
#     x, y = coordinate[0], coordinate[1]
#
#     a = example.coordinates_sequence((14, 14))
#     b = example.eight_coordinate_structure(state=current_board, coordinates_sequence=a, num=2, color=False)
#     c = [(15, 15), (16, 16), (17, 17), (18, 18)]
#     d = example.coordinate_structure(state=current_board,coordinates=c,color=False)
#
#     print(a)
#     print(b)
#     print(d)
#     print(x, y)
#
#
# if __name__ == "__main__":
#     brain_turn()
from operator import attrgetter


a = 1
b = 2
c = 3
d = a
e = [a,b,c]
e.remove(d)
print(e)

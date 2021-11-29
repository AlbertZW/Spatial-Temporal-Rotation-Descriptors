import sys

sys.path.extend(['../'])
from graph import tools

num_node = 29
self_link = [(i, i) for i in range(num_node)]
inward_ori_index = [
                # joints of the 2 arms
                (1, 2), (1, 3), (2, 3), (2, 4), (3, 4), (4, 5),
                (6, 7), (6, 8), (7, 8), (7, 9), (8, 9), (9, 10),
                # shoulders and chest
                (5, 11), (11, 13), (11, 16), (11, 15),
                (10, 12), (12, 14), (12, 17), (12, 15),
                # neck
                (13, 19), (14, 19), (18, 19),
                # spine and waist
                (16, 20), (17, 20), (20, 21), (20, 22),
                (21, 23), (22, 23), (23, 24), (23, 25),
                # 2 legs
                (24, 26), (26, 27), (25, 28), (28, 29)]
inward = [(i - 1, j - 1) for (i, j) in inward_ori_index]
outward = [(j, i) for (i, j) in inward]
neighbor = inward + outward


class Graph:
    def __init__(self, labeling_mode='spatial'):
        self.A = self.get_adjacency_matrix(labeling_mode)
        self.num_node = num_node
        self.self_link = self_link
        self.inward = inward
        self.outward = outward
        self.neighbor = neighbor

    def get_adjacency_matrix(self, labeling_mode=None):
        if labeling_mode is None:
            return self.A
        if labeling_mode == 'spatial':
            A = tools.get_spatial_graph(num_node, self_link, inward, outward)
        else:
            raise ValueError()
        return A


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import os

    # os.environ['DISPLAY'] = 'localhost:11.0'
    A = Graph('spatial').get_adjacency_matrix()
    for i in A:
        plt.imshow(i, cmap='gray')
        plt.show()
    print(A)

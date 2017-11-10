# ----------------------------------------------------------------------
# Rubik's cube simulator
# Numpy is used for face representation and operation
# Matplotlib only for plotting
# Written by Miguel Hernando (2017)
# The aim of this code is to give a simple rubik cube simulator to
# test Discrete Planning Techniques.
# The code was developed for AI teaching purpose.
# Universidad Politécnica de Madrid

import numpy as np
import matplotlib.pyplot as plt
import random
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib import colors

'''
Face State order as it is internally represented
    | 4 |
| 0 | 1 | 2 | 3 |
    | 5 |
Each face is represented by state matrix (NxN) and each cell is an integuer (0-5). 
Row and columns are disposed with the origin at the upper left corner, 
with faces disposed as the unfolded cube states. 

Rotations are referred to axis relative faces.
The outward-pointing normal of face 1 is the X axis.
The outward-pointing normal of face 2 is the Y axis.
The outward-pointing normal of face 4 is the Z axis.
 
Rotations are considered positive if they are ccw around the axis (math positive rotation)
The  cube slices are considered as layers. The upper layer (faces 1, 2 or 4) have index 0, while de 
backward layers (3,0,5) have index N-1 (N is the cube dimension)

Initial colors have the same index than their respective faces
'''

def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a

class RubCube:
    # face + rotation, face -, lateral faces (index, [tuple 1] [tuple2) tomando como base la gira +
    # giro X
    F_axis = {'front': 1, 'back': 3, 'faces': ((2, (0, 1), (-1, 0)),
                                               (4, (-1, 0), (0, -1)),
                                               (0, (0, -1), (1, 0)),
                                               (5, (1, 0), (0,
                                                            1)))}  # giro F realizado en la cara 1  capa i afecta a la i*[0,i], (0...N)*[-i 0]
    # giro Y
    R_axis = {'front': 2, 'back': 0, 'faces': ((3, (0, 1), (-1, 0)),
                                               (4, (0, -1), (1, 0)),
                                               (1, (0, -1), (1, 0)),
                                               (5, (0, -1), (1,
                                                             0)))}  # giro R realizado en la cara 2  capa i afecta a la i*[0,i], (0...N)*[-i 0]
    # giro Z
    U_axis = {'front': 4, 'back': 5, 'faces': ((0, (1, 0), (0, 1)),
                                               (1, (1, 0), (0, 1)),
                                               (2, (1, 0), (0, 1)),
                                               (3, (1, 0), (0,
                                                            1)))}  # giro U realizado en la cara 4  capa i afecta a la i*[0,i], (0...N)*[-i 0]
    axis_dict = {'x': F_axis, 'y': R_axis, 'z': U_axis}

    def __init__(self, N=3):
        self._N = N
        self.reset()

    def rotate_90(self, axis_name='x', n=0, n_rot=1):
        '''rotates 90*n_rot around one axis ('x','y','z') the layer n'''
        if axis_name not in self.axis_dict:
            return
        axis = self.axis_dict[axis_name]
        if n == 0:  # rotate the front face
            self._state[axis['front']] = np.rot90(self._state[axis['front']], k=n_rot)
        if n == self._N - 1:
            self._state[axis['back']] = np.rot90(self._state[axis['back']], k=n_rot)
        aux = []
        for f in axis['faces']:
            if f[1][0] > 0:  # row +
                r = self._state[f[0]][n, ::f[2][1]]
            elif f[1][0] < 0:  # row -
                r = self._state[f[0]][-(n + 1), ::f[2][1]]
            elif f[1][1] > 0:  # column +
                r = self._state[f[0]][::f[2][0], n]
            else:
                r = self._state[f[0]][::f[2][0], -(n + 1)]
            aux.append(r)
        raux = np.roll(np.array(aux), (self._N) * n_rot)
        
        for i,f in enumerate(axis['faces']):
            r = raux[i]
            if f[1][0] > 0:  # row +
                self._state[f[0]][n, ::f[2][1]] = r
            elif f[1][0] < 0:  # row -
                self._state[f[0]][-(n + 1), ::f[2][1]] = r
            elif f[1][1] > 0:  # column +
                self._state[f[0]][::f[2][0], n] = r
            else:
                self._state[f[0]][::f[2][0], -(n + 1)] = r

    def set_State(self, state):
        self._state = np.array(state)

    def get_State(self):
        return totuple(self._state)

    def plot(self, block=True):
        plot_list = ((1, 4), (4, 0), (5, 1), (6, 2), (7, 3), (9, 5))
        color_map = colors.ListedColormap(['#00008f', '#cf0000', '#009f0f', '#ff6f00', 'w', '#ffcf00'], 6)
        fig = plt.figure(1, (8., 8.))
        grid = ImageGrid(fig, 111,  # similar to subplot(111)
                         nrows_ncols=(3, 4),  # creates 2x2 grid of axes
                         axes_pad=0.1,  # pad between axes in inch.
                         )
        for p in plot_list:
            grid[p[0]].matshow(self._state[p[1]], vmin=0, vmax=5, cmap=color_map)
        plt.show(block=block)

    def reset(self):
        self._state = []
        for i in range(6):
            self._state.append(i * np.ones((self._N, self._N), dtype=np.int8))
    def randomMoves(self, num):
        moves=[]
        for i in range(num):
            x = random.choice(('x','y','z'))
            num = random.randint(0, self._N - 1)
            n_rot = random.randint(-1,2)
            self.rotate_90(x,num,n_rot)
            moves.append((x,num,n_rot))
        return moves



if __name__ == '__main__':
    import sys

    try:
        N = int(sys.argv[1])
    except:
        N = 3

    a = RubCube(N)
    a.rotate_90('x', 0, -1)
    a.rotate_90('y', 0, )
    a.rotate_90('z', 0, -1)

    c = a.get_State()
    print(c)
    a.plot()
    a.reset()
    a.plot()
    m=a.randomMoves(5)
    print(m)
    a.plot()
    for x in reversed(m):
        a.rotate_90(x[0],x[1],-x[2])
    a.plot()

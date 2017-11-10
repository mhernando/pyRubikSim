import rub_cube as rb


class Node:
    def __init__(self, state, g, h, action, parent):
        self.state=state
        self.g=g
        self.h=h
        self.f=g+h
        self.parent=parent
        self.action=action
    def __eq__(self, other):
        return self.state == other.state
    def __ne__(self, other):
        return self.state != other.state
    def __repr__(self):
        return "Node value f: %d  "%self.f
    #para ordenar una lista-->open.sort(key=lambda o: o.f)

class Astar:
    def __init__(self,cube):
        self.cube=cube
        self.closed=[]
        self.open=[]
        self.goal=cube.get_State()

    def heur(self,state):
        #estimation of cost to... one movement is cost 1
        #thus the estimation sould be n_diferent/(4*_N)
        #because one movement provoques 4*_N different colors
        d=0
        for i, x in enumerate(state):
            a=[xxx for xx in x for xxx in xx]
            d+=sum(1 for e in a if e!=i)
        return d/(4*self.cube._N)

    def heurDijkstra(self, state):
        return 0

    def getNeighbours(self,n_state):
        neigh=[]
        for a in "xyz":
            for n in range(self.cube._N):
                for n_rot in (-1,1):
                    self.cube.set_State(n_state.state)
                    self.cube.rotate_90(a,n,n_rot)
                    node=Node(self.cube.get_State(),
                              n_state.g+1, #current cost + 1
                              0, #estimation not computed yet
                              (a,n,n_rot), #action
                              n_state) #parent
                    neigh.append(node)
        return neigh
    @staticmethod
    def obtainPathTo(n_state):
        act=[]
        while n_state:
            act.append(n_state.action)
            n_state=n_state.parent
        return act[-2::-1]
    def solve(self, init):
        self.closed=[]
        self.open=[Node(init,0,self.heur(init),("x",0,0),None),]
        while self.open:
            print("explorados: "+str(len(self.closed)) + " Vivos: "+ str(len(self.open))+
                  "mejor f: "+str(self.open[0].f))
            #ordeno abiertos
            self.open.sort(key=lambda o: o.f)
            # extraigo el mejor y lo paso a cerrados
            current=self.open.pop(0)
            self.closed.append(current)
            if current.state==self.goal:
                return self.obtainPathTo(current)
            for n in self.getNeighbours(current):
                #si ya explorado paso de el
                if n in self.closed:
                    continue
                #calculo su g como +1 al actual
                if n in self.open:
                    #compruebo si el coste actual es mejor
                    ind=self.open.index(n)
                    on=self.open[ind]
                    if on.g > n.g: #actualizo el nodo antiguo
                        n.h = on.h
                        n.f = n.h + n.g
                        self.open[ind]=n
                else: #es un nuevo nodo,
                    #calculo h y fy lo agrego
                    n.h = self.heur(n.state)
                    n.f = n.h + n.g
                    self.open.append(n)
        return None


a=rb.RubCube()
c={}
d1=a.get_State()
a.rotate_90('x',0,1)
d2=a.get_State()
a.set_State(d1)
a.rotate_90('x',0,-3)
d3=a.get_State()

print(d1)
print(d2)
print(d3)
n1=Node(d1,2,5,('x',2,2),None)
n2=Node(d2,1,1,('x',2,2),None)
n3=Node(d3,3,0,('x',2,2),None)
if n2 == n3:
    print("d2 y d3 SON IGUALES")
if  n1 == n3:
    print("d1 y d3 SON IGUALES")
open=[n1, n2]


if n3 in open:
    print("Ya esta n3 en open")
print(str(open))
open.sort(key=lambda o: o.f)
print(str(open))
n=open.pop(0)
print(n)
print(str(open))
b=rb.RubCube(3)
sol=Astar(b)
b.rotate_90('x',0,1)
b.rotate_90('y',1,1)
b.plot()
#b.rotate_90('y')
#b.rotate_90('z',1)
print("Sol:" , sol.solve(b.get_State()))
b.reset()
b.randomMoves(4)
b.plot()
#b.rotate_90('y')
#b.rotate_90('z',1)
print("Sol:" , sol.solve(b.get_State()))
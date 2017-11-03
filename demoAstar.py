from rub_cube import RubCube

def distance(state):
    d=0
    for i, x in enumerate(state):
        d+=(x!=i).sum()
    return d
def createDescendants(parent, N=3):
    desc=[]
    for ax in 'xyz':
        for n in range(N):
            for n_rot in (-1,1):
                a.set_State(parent)
                a.rotate_90(ax,n,n_rot)
                desc.append(a.get_State())
    return desc

a=RubCube()
end=a.get_State()
print(distance(end))
a.rotate_90('x',1,1)
print(distance(a.get_State()))

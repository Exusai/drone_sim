import matplotlib.pyplot as plt


ax = plt.axes(projection='3d')
ax.plot([0, 0, 0],[0, 0, 2], [0,1,1], )
ax.set_label("0")
ax.plot([0, 0, 2, 3],[0, 0, 0, 0], [0,2.5,3, 5])
#ax.plot([[0, -2, 2],[0, 0, 0], [0,2.5,3]])
ax.set_label("1")
ax.set_xlim(-1, 1)
ax.set_ylim(-.2, 2)
ax.set_zlim(0, 2)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()
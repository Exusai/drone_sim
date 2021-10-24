import numpy as np
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


D = np.genfromtxt( "DP2.csv", delimiter=' ')
print(D.shape)

XD = D[:,0]
XO = D[:,1]

YD = D[:,2]
YO = D[:,3]

ZD = D[:,4]
ZO = D[:,5]

OD = D[:,6]
OO = D[:,7]


fig, axs = plt.subplots(4)


axs[0].plot(XD, color="red", label="Deseada")
axs[0].plot(XO, color="blue", label="Obtenida")
axs[0].set_ylabel( "X (m)" )
axs[0].grid()
axs[0].legend()


axs[1].plot(YD, color="red")
axs[1].plot(YO, color="blue")
axs[1].set_ylabel( "Y (m)" )
axs[1].grid()



axs[2].plot(ZD, color="red")
axs[2].plot(ZO, color="blue")
xmin, xmax = axs[2].get_xlim( )
ymin, ymax = axs[2].get_ylim( )
axs[2].set_xlim( xmin, xmax )

axs[2].set_ylabel( "Altura (m)" )
axs[2].grid()



axs[3].plot(OD, color="red")
axs[3].plot(OO, color="blue")
axs[3].set_xlabel( "Muestras" )
axs[3].set_ylabel( "Orientación eje Z (°)" )
axs[3].grid()



plt.show()


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(XD,YD,ZD, color="red", label="Deseada")
ax.plot(XO,YO,ZO, color="blue", label="Obtenida")
ax.set_xlabel( "X (m)" )
ax.set_ylabel( "Y (m)" )
ax.set_zlabel( "Altura (m)" )
ax.legend()




plt.show()

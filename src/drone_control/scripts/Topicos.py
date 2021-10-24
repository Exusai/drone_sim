#!/usr/bin/env python
# license removed for brevity
import rospy
import time
import numpy as np
import BebopLib as bl
#import tf
#import BebopLib as bl
#from std_msgs.msg import String
#from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
#from nav_msgs.msg import Odometry
#from sensor_msgs.msg import Range
from std_msgs.msg import Int32


#Librerias para pose ardrone en simulador
from tf2_msgs.msg import TFMessage

tt = TFMessage()
x_p = 0
y_p = 0
z_p = 0 
z_o = 0

#Callback de pose y orientacion simulador
def pose_callback(data):
    global x_p, y_p, z_o, z_p
    x_p = data.transforms[0].transform.translation.x
    y_p = data.transforms[0].transform.translation.y
    z_p = data.transforms[1].transform.translation.z
    z_o = data.transforms[0].transform.rotation.z

def enviar_velocidad(vx,vy,vz,vaz):
	vel_msg = Twist()
	vel_msg.linear.x = float(vx)
	vel_msg.linear.y = float(vy)
	vel_msg.linear.z = float(vz)
	vel_msg.angular.z = float(vaz)
	vel_pub.publish(vel_msg)

def receive_tf(data):
    global tt
    tt = data  



def trayectoria():
    
    global vel_pub

    T = TFMessage()
     #Datos control x
    kpx=5
    kdx=6
    dzn = 0.05
    satx=1.0
    #Datos control x

     #Datos control x
    kpy=5
    kdy=6
    dzn = 0.05
    saty=1.0
    #Datos control x


    #Datos control z
    kpz = 2
    kdz = 0.8
    satz = 0.8
    dzz = 0.02
    #Datos control z

    
    m = 1.477
    g = 9.81

    cp = np.array([[4.0,4.0,2.0,0.0],
    [0.0,0.0,2.0,0.0],
    [0.0,0.0,1.5,0.0],
    [0.0,0.0,1.5,0.0]])

    rospy.init_node('Trayectoria', anonymous=True)
    pose_sub = rospy.Subscriber("/tf", TFMessage , pose_callback)
    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rate = rospy.Rate(10) # 10hz
    opt = 2
    i = 1
    step = 1
    
    
    archivo = open("Datos.txt","w")
    while not rospy.is_shutdown():
        
        vz = bl.PDz(cp[0][2], z_p, kpz,kdz,satz, dzz)
        vx = bl.PDx(cp[0][0],x_p,kpx,kdx,satx,dzn,vz, m, g)
        vy = bl.PDy(cp[0][1],y_p,kpy,kdy,saty,dzn,vz, m, g)
        archivo.write(str(cp[0][0]) + " " + str(x_p) + " " + str(cp[0][1]) + " " + str(y_p) +  " " + str(cp[0][2]) +  " " + str(z_p) +  " " + str(cp[0][3]) + " "+ str(z_o) + "\n" )
        enviar_velocidad(vx,vy,vz,0.0)
        #vx = bl.PDx(cp[0][0],x_p,kpx,kdx,satx,dzn,vz, m, g)
        #vy = bl.PDy(cp[0][1],y_p,kpx,kdx,satx,dzn,vz, m, g)

        #print(tt.transforms)
        print("X")
        print(x_p)
        print("Y")
        print(y_p)
        print("Altura")
        print(z_p)
        rate.sleep()
    archivo.close()

        
       
    
if __name__ == '__main__':
    try:
        trayectoria()
    except rospy.ROSInterruptException:
        pass
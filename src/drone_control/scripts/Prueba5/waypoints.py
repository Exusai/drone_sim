#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

from pickle import HIGHEST_PROTOCOL
import BebopLib as bl
#import numpy as np
import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from ardrone_autonomy.msg import Navdata
from tf2_msgs.msg import TFMessage

x_p = 0
y_p = 0
z_p = 0
z_o = 0

init_set = False
x_init = 0
y_init = 0

#Callback de pose y orientacion simulador
def pose_callback(data):
    global x_p, y_p, z_p
    global init_set, x_init, y_init

    """ x_p = data.transforms[0].transform.translation.x
    y_p = data.transforms[0].transform.translation.y
    z_p = data.transforms[1].transform.translation.z """

    if not init_set:
        x_init = data.transforms[0].transform.translation.x
        y_init = data.transforms[0].transform.translation.y
        init_set = True

    x_p = data.transforms[0].transform.translation.x - x_init
    y_p = data.transforms[0].transform.translation.y - y_init
    z_p = data.transforms[1].transform.translation.z
  
def rot_callback(data):
    global z_o
    z_o = data.rotZ

def despegar_pub():
    takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
    takeoff_pub.publish(Empty())

def aterrizar_pub():
    land_pub = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
    land_pub.publish(Empty())

""" def enviar_velocidad(vx,vy,vz,vaz):
    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    vel_msg.linear.x = float(vx)
    vel_msg.linear.y = float(vy)
    vel_msg.linear.z = float(vz)
    vel_msg.angular.z = float(vaz)
    vel_pub.publish(vel_msg) """

def enviar_velocidad(vx,vy,vz,vaz):
	vel_msg = Twist()
	vel_msg.linear.x = float(vx)
	vel_msg.linear.y = float(vy)
	vel_msg.linear.z = float(vz)
	vel_msg.angular.z = float(vaz)
	vel_pub.publish(vel_msg)

### Waypoints ###
waypoints = [
    [3, 2],
    [2, 5],
    [6, 6],
]

### my vars ###
hover_height = 2


disp = True

def controller():
    global x_p, y_p, z_p, z_o
    
    #Datos control x
    kpx=5
    kdx=6
    dzn = 0.05
    satx=1.0
    #Datos control x

    #Datos control y
    kpy=5
    kdy=6
    dzn = 0.05
    saty=1.0
    #Datos control y

    #Datos control z
    kpz = 2
    kdz = 0.8
    satz = 0.8
    dzz = 0.02
    #Datos control z

    #Datos control zo
    kpzo = 0.03
    kdzo = 0.09
    satzo = 0.4
    dzo = 1
    #Datos control zo
    
    m = 1.477
    g = 9.81

    """ vz = bl.PDz(hover_height, z_p, kpz, kdz, satz, dzz)
    vx = bl.PDx(3, x_p, kpx, kdx, satx, dzn, vz, m, g)
    vy = bl.PDy(0, y_p, kpy, kdy, saty, dzn, vz, m, g)
    vaz = bl.PDyaw(0, z_o, kpzo, kdzo, satzo, dzo) """

    vx = bl.control_P(0, x_p, kpx, satx, dzn)
    vy = bl.control_P(0, y_p, kpy, saty, dzn)
    vz = bl.control_P(hover_height, z_p, kpz, satz, dzz)
    vaz = 0

    print("Error z: ", (hover_height-z_p))
            
    #print("Pose")
    #print( "X : " + "{0:.2f}".format(x_p) + " Y : "+ "{0:.2f}".format(y_p) + " Oz : " + "{0:.2f}".format(z_o) + " Z : " + "{0:.2f}".format(z_p) )
    print("Vel")
    print("vx : "+ "{0:.2f}".format(vx) + " vy : "+ "{0:.2f}".format(vy) +  " vaz : "+ "{0:.2f}".format(vaz)  + " vz : "+ "{0:.2f}".format(vz) )
    
    enviar_velocidad(vx, vy, vz, 0)


if __name__ == '__main__':
    try:
        print("S T A R T")

        rospy.init_node('WayPoints', anonymous=False)
        #Subscribers
        pose_sub = rospy.Subscriber("/tf", TFMessage , pose_callback)
        rot_sub = rospy.Subscriber("/ardrone/navdata", Navdata, rot_callback)
        #Publishers
        vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)  #/ardrone/cmd_vel
        land_pub = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
        takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)     

        rate = rospy.Rate(10) # 10hz

        print("Ready to fly")
               
        while not rospy.is_shutdown():
            controller()
            rate.sleep()
        
    except rospy.ROSInterruptException:
        pass


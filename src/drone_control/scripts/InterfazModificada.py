#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
from tkinter import *
from tkinter import ttk
import tk 
import math

import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from ardrone_autonomy.msg import Navdata
from std_msgs.msg import Float32MultiArray
from tf2_msgs.msg import TFMessage


root = Tk()
root.title("ardrone Interface")

mainframe = ttk.Frame(root, padding ="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
mainframe.columnconfigure(0,weight=1)

rospy.init_node('ardroneGUI', anonymous=False)


x_p = StringVar()
y_p = StringVar()
z_p = StringVar()
z_o = StringVar()

init_set = False
x_init = 0
y_init = 0


#Callback de pose y orientacion simulador
def pose_callback(data):
    global x_p, y_p, z_p, init_set, x_init, y_init

    if not init_set:
        x_init = data.transforms[0].transform.translation.x
        y_init = data.transforms[0].transform.translation.y
        init_set = True

    z_p.set("{0:.2f}".format(data.transforms[1].transform.translation.z))
    y_p.set("{0:.2f}".format(data.transforms[0].transform.translation.y - y_init))
    x_p.set("{0:.2f}".format(data.transforms[0].transform.translation.x - x_init))



  
def rot_callback(data):
    global z_o
    z_o.set("{0:.2f}".format(data.rotZ))

#Subscribers
pose_sub = rospy.Subscriber("/tf", TFMessage , pose_callback)
rot_sub = rospy.Subscriber("/ardrone/navdata", Navdata, rot_callback)

#Publishers
vel_pub = rospy.Publisher('/ardrone/cmd_vel', Twist, queue_size=10)
land_pub = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)

def despegar_pub():
    takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
    takeoff_pub.publish(Empty())

def aterrizar_pub():
    land_pub = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
    ttk.Label(mainframe, text="              ").grid(column=3, row=1, sticky=W)
    ttk.Label(mainframe, text="Land").grid(column=3, row=1, sticky=W)
    land_pub.publish(Empty())


def enviar_velocidad(vx,vy,vz,vaz):
    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    vel_msg.linear.x = float(vx)
    vel_msg.linear.y = float(vy)
    vel_msg.linear.z = float(vz)
    vel_msg.angular.z = float(vaz)
    vel_pub.publish(vel_msg)


def hover_pub():
    enviar_velocidad(0.0,0.0,0.0,0.0)

def ccw_pub():
    enviar_velocidad(0.0,0.0,0.0,1.0)

def forward_pub():
    enviar_velocidad(1.0,0.0,0.0,0.0)

def cw_pub():
    enviar_velocidad(0.0,0.0,0.0,-1.0)

def left_pub():
    enviar_velocidad(0.0,1.0,0.0,0.0)

def right_pub():
    enviar_velocidad(0.0,-1.0,0.0,0.0)

def up_pub():
    enviar_velocidad(0.0,0.0,1.0,0.0)

def backward_pub():
    enviar_velocidad(-1.0,0.0,0.0,0.0)

def down_pub():
    enviar_velocidad(0.0,0.0,-1.0,0.0)


#-------------- Despliegue datos de odometria y altura -------------------------
ttk.Label(mainframe, textvariable=x_p).grid(column=1, row=2, sticky=(W,E))
ttk.Label(mainframe, textvariable=y_p).grid(column=2, row=2, sticky=(W,E))
ttk.Label(mainframe, textvariable=z_p).grid(column=3, row=2, sticky=(W,E))
ttk.Label(mainframe, textvariable=z_o).grid(column=4, row=2, sticky=(W,E))

ttk.Label(mainframe, text="X (m)").grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, text="Y (m)").grid(column=2, row=3, sticky=W)
ttk.Label(mainframe, text="Z (m)").grid(column=3, row=3, sticky=W)
ttk.Label(mainframe, text="Yaw (°)").grid(column=4, row=3, sticky=W)
#-------------- Despliegue datos de odometria y altura -------------------------

#---------------------------- Botones de Control -------------------------------

ttk.Button(mainframe, text="Giro CCW", command=ccw_pub).grid(column=1, row=5, sticky=W)
ttk.Button(mainframe, text="Adelante", command=forward_pub).grid(column=2, row=5, sticky=W)
ttk.Button(mainframe, text="Giro CW", command=cw_pub).grid(column=3, row=5, sticky=W)


ttk.Button(mainframe, text="Izquierda", command=left_pub).grid(column=1, row=6, sticky=W)
ttk.Button(mainframe, text="Hover", command=hover_pub).grid(column=2, row=6, sticky=W)
ttk.Button(mainframe, text="Derecha", command=right_pub).grid(column=3, row=6, sticky=W)

ttk.Button(mainframe, text="Arriba", command=up_pub).grid(column=1, row=7, sticky=W)
ttk.Button(mainframe, text="Atras", command=backward_pub).grid(column=2, row=7, sticky=W)
ttk.Button(mainframe, text="Abajo", command=down_pub).grid(column=3, row=7, sticky=W)
#---------------------------- Botones de Control -------------------------------



ttk.Button(mainframe, text="Take Off", command=despegar_pub).grid(column=3, row=4, sticky=W)
ttk.Button(mainframe, text="Land", command=aterrizar_pub).grid(column=2, row=4, sticky=W)

ttk.Label(mainframe, text="1").grid(column=3, row=1, sticky=W)



for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

#root.bind('<Return>',calculate)

root.mainloop()

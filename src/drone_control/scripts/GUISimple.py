#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from Tkinter import *
import ttk
import math

import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

root = Tk()
root.title("Bebop Interface 2 Drones")

mainframe = ttk.Frame(root, padding ="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
mainframe.columnconfigure(0,weight=1)

rospy.init_node('VF', anonymous=False)

x_odom = StringVar()
y_odom = StringVar()
z_odom = StringVar()
yaw_odom = StringVar()
odom_var=Odometry()

x_b1 = StringVar()
y_b1 = StringVar()
z_b1 = StringVar()
yaw_b1 = StringVar()
odom_d1=Odometry()


def takeoff_pub():
    takeoff_pub1 = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
    #takeoff_pub2 = rospy.Publisher('/b2/takeoff', Empty, queue_size=1)
    ttk.Label(mainframe, text="          ").grid(column=3, row=1, sticky=W)
    ttk.Label(mainframe, text="Take Off").grid(column=3, row=1, sticky=W)
    takeoff_pub1.publish(Empty())
    #takeoff_pub2.publish(Empty())

def land_pub():
    land_pub1 = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
    #land_pub2 = rospy.Publisher('/b2/land', Empty, queue_size=1)
    ttk.Label(mainframe, text="              ").grid(column=3, row=1, sticky=W)
    ttk.Label(mainframe, text="Land").grid(column=3, row=1, sticky=W)
    land_pub1.publish(Empty())
    #land_pub2.publish(Empty())


#feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
#feet_entry.grid(column=2, row=1, sticky=(W,E))



ttk.Button(mainframe, text="Take Off", command=takeoff_pub).grid(column=3, row=4, sticky=W)
ttk.Button(mainframe, text="Land", command=land_pub).grid(column=2, row=4, sticky=W)

ttk.Label(mainframe, text="1").grid(column=3, row=1, sticky=W)



for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

#feet_entry.focus()
#root.bind('<Return>',calculate)

root.mainloop()
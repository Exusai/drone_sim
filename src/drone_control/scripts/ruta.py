#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
import numpy as np
import rospy
from std_msgs.msg import Empty
from geometry_msgs.msg import Twist
from ardrone_autonomy.msg import Navdata
from tf2_msgs.msg import TFMessage
import matplotlib.pyplot as plt

x_p = 0
y_p = 0
z_p = 0
z_o = 0

init_set = False
x_init = 0
y_init = 0

x_vect = []
y_vect = []
z_vect = []


#Callback de pose y orientacion simulador
def pose_callback(data):
    global x_p, y_p, z_p, init_set, x_init, y_init
    global x_vect, y_vect, z_vect

    if not init_set:
        x_init = data.transforms[0].transform.translation.x
        y_init = data.transforms[0].transform.translation.y
        init_set = True

    x_p = data.transforms[0].transform.translation.x - x_init
    y_p = data.transforms[0].transform.translation.y - y_init
    z_p = data.transforms[1].transform.translation.z

    x_vect.append(x_p)
    y_vect.append(y_p)
    z_vect.append(z_p)

    
  
def rot_callback(data):
    global z_o
    z_o = data.rotZ

def despegar_pub():
    takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)
    takeoff_pub.publish(Empty())

def aterrizar_pub():
    land_pub = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
    land_pub.publish(Empty())


def enviar_velocidad(vx,vy,vz,vaz):
    vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()
    vel_msg.linear.x = float(vx)
    vel_msg.linear.y = float(vy)
    vel_msg.linear.z = float(vz)
    vel_msg.angular.z = float(vaz)
    vel_pub.publish(vel_msg)

step = 0
x_target = 2
z_target = 2.5
error_x = 0
error_y = 0
error_z = 0
error_zo = 0

def norm_vel(vel):
    if vel > -0.1 and vel < 0.1:
        return 0.0
    else: return vel

disp = True
def controller():
    global step, x_target, error_x, error_y, error_z, z_target, z_o, error_zo
    kp = 2

    global disp
    global x_vect, y_vect, z_vect

    if step == 0:
        print('Despegando')
        time = rospy.get_time()
        wait = rospy.Duration(4).to_sec()
        end_time = time + wait

        while rospy.get_time() < end_time:
            despegar_pub()

        print("Iniciando Ruta")
        step = step + 1

    if step == 1:
        if disp == True:
            print("Elevandose a 2.5m", )
            disp = False
        
        error_z = z_target - z_p
        vel_z = kp * error_z
        
        error_y = 0 - y_p
        vel_y = .5 * error_y

        error_x = 0 - x_p
        vel_x = .5 * error_x
        
        error_zo = 0 - z_o
        vel_zo = 1 * error_zo

        vel_z = norm_vel(vel_z)
        vel_y = norm_vel(vel_y)
        vel_x = norm_vel(vel_x)
        #vel_zo = norm_vel(vel_zo)

        """ print("////////////")
        print("x:   {0:.4f}".format(vel_x))
        print("z:   {0:.4f}".format(vel_z))
        print("y:   {0:.4f}".format(vel_y))
        print("zo:  {0:.4f}".format(vel_zo)) """

        enviar_velocidad(vel_x,vel_y,vel_z,vel_zo)
        
        if error_z < 0.1 and error_z > -0.1:
            step = step + 1
            disp = True
            print("Altura alcanzada")

    if step == 2:
        if disp == True:
            print("Avanzando 2m hacia adelante", )
            disp = False

        error_z = z_target - z_p
        vel_z = kp * error_z
        
        error_y = 0 - y_p
        vel_y = .5 * error_y

        error_x = 2 - x_p
        vel_x = .5 * error_x
        
        error_zo = 0 - z_o
        vel_zo = 1 * error_zo

        vel_z = norm_vel(vel_z)
        vel_y = norm_vel(vel_y)
        vel_x = norm_vel(vel_x)
        
        enviar_velocidad(vel_x,vel_y,vel_z,vel_zo)

        if error_x < 0.2 and error_x > -0.2:
            step = step + 1
            print("Objetivo alcanzado")
            ax = plt.axes(projection='3d')
            ax.plot([0, 0, 2],[0, 0, 0], [0,2.5,2.5])
            #ax.set_label('Ruta deseada')
            ax.plot(x_vect, y_vect, z_vect)
            #ax.set_label('Ruta realizada')
            ax.set_xlim(-.2, 2.5)
            ax.set_ylim(-1, 1)
            ax.set_zlim(0, 3)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            plt.show()
    
    if step == 3:
        error_z = z_target - z_p
        vel_z = kp * error_z
        
        error_y = 0 - y_p
        vel_y = .5 * error_y

        error_x = 2 - x_p
        vel_x = .5 * error_x
        
        error_zo = 0 - z_o
        vel_zo = 1 * error_zo

        #vel_z = norm_vel(vel_z)
        #vel_y = norm_vel(vel_y)
        #vel_x = norm_vel(vel_x)
        
        enviar_velocidad(vel_x,vel_y,vel_z,vel_zo)

prevTime = 0
def controller2():
    global step, x_target, error_x, error_y, error_z, z_target, z_o, error_zo
    kp = 1.5
    global prevTime
    global disp
    global x_vect, y_vect, z_vect
    if step == 0:
        print('Despegando')
        time = rospy.get_time()
        wait = rospy.Duration(4).to_sec()
        end_time = time + wait

        while rospy.get_time() < end_time:
            despegar_pub()

        print("Iniciando Ruta")
        step = step + 1
        
    if step == 1:
        if disp == True:
            print("Elevandose a 1m", )
            disp = False
        
        error_z = 1 - z_p
        vel_z = kp * error_z
        
        error_y = 0 - y_p
        vel_y = 1 * error_y

        error_x = 0 - x_p
        vel_x = 1 * error_x
        
        error_zo = 0 - z_o
        vel_zo = 1 * error_zo

        """ vel_z = norm_vel(vel_z)
        vel_y = norm_vel(vel_y)
        vel_x = norm_vel(vel_x) """
        #vel_zo = norm_vel(vel_zo)

        """ print("////////////")
        print("x:   {0:.4f}".format(vel_x))
        print("z:   {0:.4f}".format(vel_z))
        print("y:   {0:.4f}".format(vel_y))
        print("zo:  {0:.4f}".format(vel_zo)) """

        enviar_velocidad(vel_x,vel_y,vel_z,vel_zo)
        
        if error_z < 0.1 and error_z > -0.1:
            step = step + 1
            disp = True
            print("Altura alcanzada")

    if step == 2:
        if disp == True:
            print("Avanzando 2m hacia la izquierda", )
            disp = False

        error_z = 1 - z_p
        vel_z = kp * error_z
        
        error_y = 2 - y_p
        vel_y = 1 * error_y

        error_x = 0 - x_p
        vel_x = 1 * error_x
        
        error_zo = 0 - z_o
        vel_zo = 1 * error_zo

        """ vel_z = norm_vel(vel_z)
        vel_y = norm_vel(vel_y)
        vel_x = norm_vel(vel_x) """
        
        enviar_velocidad(vel_x,vel_y,vel_z,vel_zo)

        if error_y < 0.2 and error_y > -0.2:
            step = step + 1
            print("Objetivo alcanzado")
            ax = plt.axes(projection='3d')
            ax.plot([0, 0, 0],[0, 0, 2], [0,1,1])
            #ax.set_label('Ruta deseada')
            ax.plot(x_vect, y_vect, z_vect)
            #ax.set_label('Ruta realizada')
            ax.set_xlim(-1, 1)
            ax.set_ylim(-.2, 2)
            ax.set_zlim(0, 2)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            plt.show()
    
    if step == 3:
        error_z = 1 - z_p
        vel_z = kp * error_z
        
        error_y = 2 - y_p
        vel_y = 1 * error_y

        error_x = 0 - x_p
        vel_x = 1 * error_x
        
        error_zo = 0 - z_o
        vel_zo = 1 * error_zo

        #vel_z = norm_vel(vel_z)
        #vel_y = norm_vel(vel_y)
        #vel_x = norm_vel(vel_x)
        
        enviar_velocidad(vel_x,vel_y,vel_z,vel_zo)


if __name__ == '__main__':
    try:
        rospy.init_node('RutaDron', anonymous=True)
        #Subscribers
        pose_sub = rospy.Subscriber("/tf", TFMessage , pose_callback)
        rot_sub = rospy.Subscriber("/ardrone/navdata", Navdata, rot_callback)
        #Publishers
        vel_pub = rospy.Publisher('/ardrone/cmd_vel', Twist, queue_size=10)
        land_pub = rospy.Publisher('/ardrone/land', Empty, queue_size=1)
        takeoff_pub = rospy.Publisher('/ardrone/takeoff', Empty, queue_size=1)     
               
        while not rospy.is_shutdown():
            controller()
            #controller2()
        
    except rospy.ROSInterruptException:
        pass


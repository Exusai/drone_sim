import math

#  -*- coding: utf-8 -*-
er_antx = 0.0
er_anty = 0.0
er_antz = 0.0 
er_antyaw = 0.0

def conv_ang(ang_d):
    cn1=-2.981e-10
    cn2=2.223e-07
    cn3=-1.798e-05
    cn4=-0.007787
    cn5=0.004498
    cp1=5.749e-10
    cp2=-5.023e-07
    cp3=0.000128
    cp4=-0.01078
    cp5=1.119

    if(ang_d < 0.0):
        ang_d=360-abs(ang_d)

    if (ang_d>=0 and ang_d<=180):
        p=cn1*pow(ang_d,4)+cn2*pow(ang_d,3)+cn3*pow(ang_d,2)+cn4*ang_d+cn5
    elif (ang_d>=180 and ang_d<=360):
        p=(cp1*pow(ang_d,4)+cp2*pow(ang_d,3)+cp3*pow(ang_d,2)+cp4*ang_d+cp5)
    
    return p

def control_P(ref,q,kp,sat,dz):
    er=ref-q
    tao=kp*er
    if abs(er)<=dz:
        tao=0.0
    if tao>sat:
        tao=sat
    if tao<-sat:
        tao=-sat
    return tao

#Controles con modelo dinamico
def PDz( q_ref, q, kp, kd, sat, death_zone):
    global er_antz
    err=q_ref-q
    der=err-er_antz
    er_antz=err
    tao=kp*err+kd*der
    if abs(err)<=death_zone:
        tao=0
    if tao>sat:
        tao=sat
    if tao<-sat:
        tao=-sat
    
    return tao
    
def PDx(q_ref, q, kp, kd, sat, death_zone, uz, m, g):
    global er_antx
    err=q_ref-q
    der=err-er_antx
    er_antx=err
    tao=(kp*err+kd*der)/( uz + (m*g))
    if abs(err)<=death_zone:
        tao=0
    if tao>sat:
        tao=sat
    if tao<-sat:
        tao=-sat
    return tao
    
def PDy(q_ref, q, kp, kd, sat, death_zone, uz, m, g):
    global er_anty
    err=q_ref-q
    der=err-er_anty
    er_anty=err
    tao=(kp*err+kd*der)/( uz + (m*g))
    if abs(err)<=death_zone:
        tao=0
    if tao>sat:
        tao=sat
    if tao<-sat:
        tao=-sat
    return tao

def PDyaw( q_ref, q, kp, kd, sat, death_zone):
    global er_antyaw
    err=q_ref-q
    der=err-er_antyaw
    er_antyaw=err
    tao=kp*err+kd*der
    if abs(err)<=death_zone:
        tao=0
    if tao>sat:
        tao=sat
    if tao<-sat:
        tao=-sat
    
    return tao


#Controles con modelo dinamico

# Distancia entre 2 puntos 3D
def dist(xi, yi, zi, xii, yii, zii):
    d = math.sqrt( pow((xii-xi),2) + pow((yii-yi),2) + pow((zii-zi),2) )
    return d
# Distancia entre dos puntos 3D

# Distancia entre dos puntos 2D
def dist2D(xi, yi, xii, yii):
    d = math.sqrt( pow((xii-xi),2) + pow((yii-yi),2) ) 
    return d
# Distancia entre dos puntos 2D

#Coordenadas cuadrante
def cuadrante( h,k, x_p, y_p, r):
    if( (x_p/r) > 1 ):
        alpha = 90
    elif( (x_p/r) < -1 ):
        alpha = 270
    else:
        if( y_p < h and x_p > k ):
            print ("Cuadrante 1")
            alpha = (math.degrees(math.asin(x_p/r)))
        elif( y_p > h and x_p > k ):
            print ("Cuadrante 2")
            alpha = (math.degrees(math.asin(x_p/r)))
            alpha = 180 - alpha
        elif( y_p > h and x_p < k ):
            print ("Cuadrante 3")
            alpha = (math.degrees(math.asin(x_p/r)))
            alpha = 180 - alpha
        elif( y_p < h and x_p < k):
            print ("Cuadrante 4")
            alpha = (math.degrees(math.asin(x_p/r)))
            alpha = 360 + alpha
    return alpha
#Coordenadas cuadrante

#Procesamiento de la orientacion
def cord(att_p):
    if (att_p <  1 and  att_p > -1):
        att_p = 0
    elif(att_p >= -179.99 and att_p <= -1):
        att_p = 360 + att_p
    else:
        att_p = att_p
    return att_p

#Procesamiento de la orientacion
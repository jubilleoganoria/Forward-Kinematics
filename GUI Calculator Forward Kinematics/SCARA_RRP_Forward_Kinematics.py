# SCARA RRP Forward Kinematics
import numpy as np
import math
import PySimpleGUI as sg
import pandas as pd

# GUI code

sg.theme('DarkRed1')

# Excel read code

EXCEL_FILE = 'SCARA RRP Forward Kinematics.xlsx'
df = pd.read_excel(EXCEL_FILE)

# Lay-out code

layout = [
    [sg.Text('Fill out the following fields:')],
     [sg.Text('a1= '),sg.InputText(key='a1', size=(20,10)), sg.Text('T1= '),sg.InputText(key='T1', size=(20,10))],
     [sg.Text('a2= '),sg.InputText(key='a2', size=(20,10)), sg.Text('T2= '),sg.InputText(key='T2', size=(20,10))],
     [sg.Text('a3= '),sg.InputText(key='a3', size=(20,10)), sg.Text('d3= '),sg.InputText(key='d3', size=(20,10))],
     [sg.Text('a4= '),sg.InputText(key='a4', size=(20,10))],
     [sg.Text('a5= '),sg.InputText(key='a5', size=(20,10))],
     [sg.Button('Solve Forward Kinematics')],
     [sg.Frame('Postion Vector: ',[[
         sg.Text('X = '), sg.InputText(key='X', size=(10,1)),
         sg.Text('Y = '), sg.InputText(key='Y', size=(10,1)),
         sg.Text('Z = '), sg.InputText(key='Z', size=(10,1))]])],
     [sg.Frame('H0_3 Transformation Matrix = ',[[sg.Output(size=(60,12))]])],
     [sg.Submit(), sg.Button('Clear Input'),sg.Exit()]
     ]

# Window Code
window = sg.Window('SCARA RRP Manipulator Forward Kinematics', layout)

def clear_input():
    for key in values:
        window[key]('')
    return None

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear Input':
        clear_input()
    if event == 'Solve Forward Kinematics':
        # Foward Kinematic Codes 
        a1 = values['a1']
        a2 = values['a2']
        a3 = values['a3']
        a4 = values['a4']
        a5 = values['a5']

        T1 = values['T1']
        T2 = values['T2']
        d3 = values['d3']

        T1 = (float(T1)/180.0)*np.pi # Theta 1 in radians
        T2 = (float(T2)/180.0)*np.pi # Theta 2 in radians

        PT = [[float(T1),(0.0/180.0)*np.pi,float(a2),float(a1)],
            [float(T2),(180.0/180.0)*np.pi,float(a4),float(a3)],
            [(0.0/180.0)*np.pi,(0.0/180.0)*np.pi,0,float(a5)+float(d3)]]

        i = 0
        H0_1 = [[np.cos(PT[i][0]),-np.sin(PT[i][0])*np.cos(PT[i][1]),np.sin(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.cos(PT[i][0])],
                [np.sin(PT[i][0]),np.cos(PT[i][0])*np.cos(PT[i][1]),-np.cos(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.sin(PT[i][0])],
                [0,np.sin(PT[i][1]),np.cos(PT[i][1]),PT[i][3]],
                [0,0,0,1]]

        i = 1
        H1_2 = [[np.cos(PT[i][0]),-np.sin(PT[i][0])*np.cos(PT[i][1]),np.sin(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.cos(PT[i][0])],
                [np.sin(PT[i][0]),np.cos(PT[i][0])*np.cos(PT[i][1]),-np.cos(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.sin(PT[i][0])],
                [0,np.sin(PT[i][1]),np.cos(PT[i][1]),PT[i][3]],
                [0,0,0,1]]

        i = 2
        H2_3 = [[np.cos(PT[i][0]),-np.sin(PT[i][0])*np.cos(PT[i][1]),np.sin(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.cos(PT[i][0])],
                [np.sin(PT[i][0]),np.cos(PT[i][0])*np.cos(PT[i][1]),-np.cos(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.sin(PT[i][0])],
                [0,np.sin(PT[i][1]),np.cos(PT[i][1]),PT[i][3]],
                [0,0,0,1]]

        # print("H0_1 =" )
        # print(np.matrix(H0_1))
        # print("H1_2 =" )
        # print(np.matrix(H1_2))
        # print("H2_3 =" )
        # print(np.matrix(H2_3))

        H0_2 = np.dot(H0_1,H1_2)
        H0_3 = np.dot(H0_2,H2_3)

        print("H0_3=")
        print(np.matrix(H0_3))

        X0_3 = H0_3[0,3]
        print("X = ")
        print (X0_3)

        Y0_3 = H0_3[1,3]
        print("Y = ")
        print (Y0_3)

        Z0_3 = H0_3[2,3]
        print("Z = ")
        print (Z0_3)

        
    if event == 'Submit' :
        df = df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data saved!')
        print(event,values)
        clear_input()
window.close()
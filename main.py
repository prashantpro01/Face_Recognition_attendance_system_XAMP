from fileinput import close
from turtle import hideturtle
import cv2
import numpy as np
import face_recognition
import os
from pymysql import *
import pymysql.cursors
from tkinter import *
from tkinter import messagebox
from datetime import *
from tkinter import messagebox

top = Tk()  
top.title('F_R B A_S')
top.geometry('800x800')
top.resizable(0,0)

label2=Label(top,text='F_R B A_S',font='Times 80').place(x=150,y=10)
label3=Label(top,text='Simplifying The Way Of Marking Attendance',font='Times 15').place(x=250,y=152)


def main():
    top.destroy
    path = 'images'
    images = []
    personName = []
    myList = os.listdir(path)
    print(myList)

    for cu_img in myList:
        current_Img = cv2.imread(f'{path}/{cu_img}')
        images.append(current_Img)
        personName.append(os.path.splitext(cu_img)[0])
    print(personName)

    def faceEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode =face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = faceEncodings(images)
    print("encoding done") 

    cap = cv2.VideoCapture(1)
    count = 0
    while True:
        ret, frame = cap.read()
        faces = cv2.resize(frame,(0,0),None,0.25,0.25)
        faces = cv2.cvtColor(faces,cv2.COLOR_BGR2RGB)

        facesCurrentFrame = face_recognition.face_locations(faces)
        encodesCurrentFrame = face_recognition.face_encodings(faces,facesCurrentFrame)

        for encodeFace, faceLoc in zip(encodesCurrentFrame,facesCurrentFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                name = personName[matchIndex].upper()
                count+=1
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
                print(count)
                if count == 1 :
                    print(name)
                    count=0  
                    A = messagebox.askyesno('HELLO '+name, 'click yes to mark your attendance')  
                    print(A) 
                    if A == True :
                        print("hi")
                        conn = connect(host="localhost",user="root",password="",db='FRBAS')
                        var = conn.cursor()
                        var.execute("insert into attendance (name,date,time) values ('"+name+"',curdate(),curtime())")
                        conn.commit()
                        cv2.destroyAllWindows()
                    else:
                        cv2.destroyAllWindows()
                           
        cv2.imshow("Camera",frame)
        if cv2.waitKey(10) == 13:
            break
    cap.release()
    cv2.destroyAllWindows()

showbtn = Button(top,text='START',activebackground='orange',width=11,height=1,font=('dk',25,'bold'),relief='raised',bd=10,bg='lime',fg='white',command=main).place(x=320,y=450)
showbtn = Button(top,text='CLOSE',activebackground='red',width=11,height=1,font=('dk',25,'bold'),relief='raised',bd=10,bg='red',fg='white',command=top.destroy).place(x=320,y=600)

top.mainloop()



import cv2
from face_detection import face
from keras.models import load_model
import numpy as np
from embedding import emb
from retreive_pymongo_data import database


label=None
a={0:0,1:0}
people={0:"aravindh",1:"jai"}
abhi=None
data=database()
e=emb()
fd=face()

print('attendance till now is ')
data.view()

model=load_model('face_reco1.MODEL')


def test():
    test_run=cv2.imread('/home/aravindh/downloads/Attendance-using-Face-master/people/jai1/1.jpg',1)
    test_run=cv2.resize(test_run,(160,160))
    test_run=test_run.astype('float')/255.0
    test_run=np.expand_dims(test_run,axis=0)
    test_run=e.calculate(test_run)
    test_run=np.expand_dims(test_run,axis=0)
    test_run=model.predict(test_run)[0]


cap=cv2.VideoCapture(0)
ret=True
#test()
while ret:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    detected,x,y,w,h=fd.detectFace(frame)

    if(detected is not None):
        f=detected
        detected=cv2.resize(detected,(160,160))
        detected=detected.astype('float')/255.0
        detected=np.expand_dims(detected,axis=0)
        feed=e.calculate(detected)
        feed=np.expand_dims(feed,axis=0)
        prediction=model.predict(feed)

        result=int(np.argmax(prediction))
        for i in people:
            if(result==i):
                label=people[i]
                if(a[i]==0):
                    data.update(label)
                a[i]=1
                abhi=i

        #data.update(label)
        cv2.putText(frame,label,(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        if(a[abhi]==1):
            cv2.putText(frame,"your attendance is complete",(x,y-30),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(252,160,39),3)
        cv2.imshow('onlyFace',f)
    cv2.imshow('frame',frame)
    if(cv2.waitKey(1) & 0XFF==ord('x')):
        break
cap.release()
cv2.destroyAllWindows()
data.export_csv()
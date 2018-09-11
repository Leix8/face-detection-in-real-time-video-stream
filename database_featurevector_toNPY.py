import os,sys
import csv
import cv2
import dlib
import numpy as np

    
def main():
    path,path_array=sys.argv[1],sys.argv[2]
    global detector,sp,facerec
    sp=dlib.shape_predictor(os.getcwd()+"/shape_predictor_68_face_landmarks.dat")
    facerec=dlib.face_recognition_model_v1(os.getcwd()+"/dlib_face_recognition_resnet_model_v1.dat")
    detector=dlib.cnn_face_detection_model_v1(os.getcwd()+"/mmod_human_face_detector.dat") 
    
    if not os.path.exists(path_array):
        os.makedirs(path_array)
    if not os.path.exists(path):
        print("cannot find database, please check input path")
        sys.exit()
    filelist=os.listdir(path)
    
    print(type(filelist),filelist)
    for filename in filelist:
        img=cv2.imread(path+"/"+filename)
        #cv2.imshow("img",img)
        #cv2.waitKey(0)
        filename=os.path.splitext(filename)[0]
        print(filename)
        face=detector(img,1)
        if len(face)!=1:
            print("multiple face detected, please check image")
            break
        else:
            shape=sp(img,face[0].rect)
            face_descriptor =facerec.compute_face_descriptor(img,shape)
            print("face descriptor_"+filename+"\n", face_descriptor)
            np.save(path_array+"/"+filename,np.array(face_descriptor))
       
            

if __name__=='__main__':
    main()
    


import sys
import os
import argparse
import cv2
import dlib
import time
import numpy as np

WINDOW_NAME = 'Gemalto'


def parse_args():
    # Parse input arguments
    desc = 'Video stream with human face detection'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--rtsp', dest='use_rtsp',
                        help='use IP CAM (remember to also set --uri)',
                        action='store_true')
    parser.add_argument('--uri', dest='rtsp_uri',
                        help='RTSP URI, e.g. rtsp://192.168.1.64:554',
                        default=None, type=str)
    parser.add_argument('--latency', dest='rtsp_latency',
                        help='latency in ms for RTSP [200]',
                        default=50, type=int)
    parser.add_argument('--usb', dest='use_usb',
                        help='use USB webcam (remember to also set --vid)',
                        action='store_true')
    parser.add_argument('--vid', dest='video_dev',
                        help='device # of USB webcam (/dev/video?) [1]',
                        default=0, type=int)
    parser.add_argument('--width', dest='image_width',
                        help='image width [1920]',
                        default=1280, type=int)
    parser.add_argument('--height', dest='image_height',
                        help='image height [1080]',
                        default=1280, type=int)
    args = parser.parse_args()
    return args


def open_cam_rtsp(uri, width, height, latency):
    gst_str = ('rtspsrc location={} latency={} ! '
               'rtph264depay ! h264parse ! omxh264dec ! '
               'nvvidconv ! '
               'video/x-raw, width=(int){}, height=(int){}, '
               'format=(string)BGRx ! '
               'videoconvert ! appsink').format(uri, latency, width, height)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)


def open_cam_usb(dev, width, height):
    # We want to set width and height here, otherwise we could just do:
    #     return cv2.VideoCapture(dev)
    gst_str = ('v4l2src device=/dev/video{} ! '
               'video/x-raw, width=(int){}, height=(int){}, '
               'format=(string)RGB ! '
               'videoconvert ! appsink').format(dev, width, height)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)


def open_cam_onboard(width, height):
    # On versions of L4T prior to 28.1, add 'flip-method=2' into gst_str
    gst_str = ('nvcamerasrc ! '
               'video/x-raw(memory:NVMM), '
               'width=(int)2592, height=(int)1458, '
               'format=(string)I420, framerate=(fraction)30/1 ! '
               'nvvidconv ! '
               'video/x-raw, width=(int){}, height=(int){}, '
               'format=(string)BGRx ! '
               'videoconvert ! appsink').format(width, height)
    return cv2.VideoCapture(gst_str, cv2.CAP_GSTREAMER)


def open_window(width, height):
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, width, height)
    cv2.moveWindow(WINDOW_NAME, 0, 0)
    cv2.setWindowTitle(WINDOW_NAME, 'Gemalto-Real time human face detection')

def recognizor(obj_vector):
    result={}
    namelist=os.listdir(path_data)
#    print(namelist)
    for name in namelist:
        data=np.load(path_data+name)
 #       print(type(obj_vector),type(data))
#        print(np.shape(np.array(obj_vector)),np.shape(data))
        result[name.split(".")[0]]=np.sqrt(np.sum(np.square(np.array(data)-np.array(obj_vector))))
     
    return(result)

def find_match(dist):
    distance=100
    result="404 not found"
    for k,d in dist.items():
        if d<distance:
            distance=d
            result=k
        if distance>0.8:
            result="not found"
    return (result)






def video_main(cap):
#show some basic information
    show_help = True
    full_scrn = False
    help_text = '"Esc" to Quit, "F" to Toggle Fullscreen'
    font = cv2.FONT_HERSHEY_PLAIN
    
#prapare frame counting and remark time 
    frame_cnt=0
    time_af,time_bf=0,0
    time_fbf,time_faf=0,0
    
#set path for save detections



#keep reading frames and do detection
    while True:
        frame_cnt=frame_cnt+1
        time_fbf=time_faf
# grab the next image frame from camera
        _, img_org = cap.read() 
#resize the image into img (for detection and propose bounding box) and img_org (for display)
        img_org=cv2.resize(img_org,(1600,1000))
        print("image size",img_org.shape[0],img_org.shape[1])
        img=cv2.resize(img_org,(320,200))
#save the axis scale for later calibration
        scale_x=img_org.shape[0]/img.shape[0]
        scale_y=img_org.shape[1]/img.shape[1]

#take subframes, to observe the time efficiency
#        if (frame_cnt%2)==1:
        if True:    #turn off subframe
            time_bf=time_af
            faces=detector(img,1)
            time_af=time.time()
            print("every two : ",time_af-time_bf)
            if len(faces)==0:
                print("no face detected")           
            
            else:
                for i in range(len(faces)):
                    face=faces[i]
                    l=face.rect.left()
                    t=face.rect.top()
                    w=face.rect.width()
                    h=face.rect.height()
                    cv2.rectangle(img_org, (int(l*scale_x),int(t*scale_y)),(int((l+w)*scale_x),int((t+h)*scale_y)),(255,0,0),2)
                    face_crop=img_org[int(t*scale_y):int((t+h)*scale_y),int(l*scale_x):int((l+w)*scale_x)]
                    cv2.imwrite(path+"/detection_"+str(len(faces)-i)+"_"+str(frame_cnt%5+1)+".jpg",face_crop)
                    
                    shape=sp(img_org,face.rect)
                    face_descriptor =facerec.compute_face_descriptor(img,shape)
#                    print("face descriptor: ", face_descriptor)
                    dist=recognizor(face_descriptor)
                    print(dist)
                    result=find_match(dist)
                    print(result)
                    cv2.putText(img_org,result,(int(l*scale_x),int(t*scale_y)),font,2.0,(255,0,0),3)
        
        
        
        
        
        
        
        
        
        
#showing help and set key         
        if show_help:
            cv2.putText(img_org, help_text, (10, 30), font,
                    2.0, (180,180,180), 4, cv2.LINE_AA)
            cv2.putText(img_org, help_text, (10, 30), font,
                        2.0, (255,255,255), 1, cv2.LINE_AA)
        cv2.imshow(WINDOW_NAME, img_org)

           
        key = cv2.waitKey(1)
        if key == 27: # ESC key: quit program
            break
        elif key == ord('H') or key == ord('h'): # toggle help message
            show_help = not show_help
        elif key == ord('F') or key == ord('f'): # toggle fullscreen
            full_scrn = not full_scrn
            if full_scrn:
                cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN,
                                      cv2.WINDOW_FULLSCREEN)
            else:
                cv2.setWindowProperty(WINDOW_NAME, cv2.WND_PROP_FULLSCREEN,
                                      cv2.WINDOW_NORMAL)
        time_faf=time.time()
        print("frame time: ", time_faf-time_fbf)
        print("******************************")
        
        


def main():
    args = parse_args()
    print('Called with args:')
    print(args)
    print('OpenCV version: {}'.format(cv2.__version__))
    global detector,sp,facerec
    sp=dlib.shape_predictor(os.getcwd()+"/shape_predictor_68_face_landmarks.dat")
    facerec=dlib.face_recognition_model_v1(os.getcwd()+"/dlib_face_recognition_resnet_model_v1.dat")
    detector=dlib.cnn_face_detection_model_v1(os.getcwd()+"/mmod_human_face_detector.dat") 
    
    global path,path_data
    path=os.getcwd()+"/DetectionImages"
    path_data=os.getcwd()+"/data/feature_vectors/"
    if not os.path.exists(path):
        os.makedirs(path)
#    detector=dlib.get_frontal_face_detector()
#    global face_cascade
#    face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

 
    if args.use_rtsp:
        cap = open_cam_rtsp(args.rtsp_uri,
                            args.image_width,
                            args.image_height,
                            args.rtsp_latency)
    elif args.use_usb:
        cap = open_cam_usb(args.video_dev,
                           args.image_width,
                           args.image_height)
    else: # by default, use the Jetson onboard camera

        cap = open_cam_onboard(args.image_width,
                               args.image_height)

    if not cap.isOpened():
        sys.exit('Failed to open camera!')

    open_window(args.image_width, args.image_height)
    video_main(cap)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

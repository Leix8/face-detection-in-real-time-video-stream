# face-detection-in-real-time-video-stream
this application enables real time human face detections build for Nvidia Jetson TX2 board. 

Pre-requisite:
1. *Python (Python 3.4 recomeended)*
2. *Opencv* 
3. *Dlib*

## Intro:
Today when we want to do face detection, we mainly have two options to build on:
1. *Haar Cascade model* 
2. *Dlib*

both these two open source tool are good for face detection from images; however, due to computation efficiency, there may be harmful delay when deleaing with video streams. 

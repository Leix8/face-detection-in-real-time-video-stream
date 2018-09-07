# face-detection-in-real-time-video-stream
this application enables real time human face detections build for Nvidia Jetson TX2 board. 

## Pre-requisite:
* Python (Python 3.4 recomeended)
* Opencv 
* Dlib

## Intro:
Today when we want to do face detection, we mainly have two options to build on:
* Haar Cascade model 
* Dlib

both these two open source tool are good for face detection from images; however, due to computation efficiency, there may be harmful delay when deleaing with video streams. This application, based on Dlib, explores and provides a more efficient output for video face detection. 

## Usage:
just run script in command line:
Python dlib-tegra-cam.py 
and it will utilize on board camera to display detection video and save detection result to a folder name DetectionImages

import cv2 as cv
import os
width = 1280
height = 800

def clear_dir(path):
    for file in os.listdir(path):
        os.remove(os.path.join(path,file))


def crop(path,x,y,w,h,filename):
    frame = path
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    w = w-10
    h = h-10
    frame = frame[int(y-h):int(y+h),int(x-w):int(x+w)] # H , W
    crop_path = 'static/output/crop/'+str(filename)+'.jpg' # cropped img path
    cv.imwrite(crop_path,frame)
    return crop_path


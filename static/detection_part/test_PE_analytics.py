# lib
import numpy as np
import pandas as pd
import cv2 as cv
import time
import torch
# manual function
from static.detection_part.condition_PE_Analytics import is_notmoving
from static.detection_part.getclass_yaml import get_classname
from static.detection_part.crop_save import crop, clear_dir
from static.detection_part.list_crop_images import insert_images
from static.count_part.Counting import  draw,is_same
from static.count_part.Contours_method import HSV_method

# define video path
global output_path, output_filename


def get_output_path():
    return output_path


def get_output_filename():
    return output_filename


global result_frame
result_frame = 'nopic'


def get_result_frame():
    return result_frame


def start_detect(path, model, saved):
    total_pellet,pellet_prev = 0 , []
    Total = pd.DataFrame(columns=["xcenter", "ycenter", "width", "height", "confidence", "name"])
    classes = get_classname()
    All = 0  # ALL amount of defect
    # List to check not moving event happens?
    current_result = []
    previous_result = []
    # define input frame resolution
    width = 1280
    height = 800
    # define to show fps (latency per sec)
    prev_frame_time = 0
    start_time = time.ctime(time.time())
    # path of crop images to detect
    images = []
    # clear directory crop for append images
    clear_dir(path='static/output/crop')
    # save section
    if saved:
        out = cv.VideoWriter('output/res_video.mp4', -1, 30.0, (width, height))
    cap = cv.VideoCapture(path)
    # loop frame input to detection
    while (cap.isOpened()):
        ret, img = cap.read()
        if ret == True:
            # get frame
            img = cv.resize(img, (width, height))
            # # counting part
            im0 = img.copy()
            roi = im0[:height, int(width / 3):int(2 * width / 3)]  # (H,W)
            # findcontours
            contours = HSV_method(roi)
            pellet_current, count_frame = draw(roi, contours)
            if is_same(pellet_prev,pellet_current): # same frame(not moving event)
                # print('its same frame')
                continue
            pellet_prev = pellet_current
            total_pellet += len(pellet_current)

            cv.imshow('count',count_frame)
            # # detection part
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            result = model(img)
            # condition to push
            temp_table = (result.pandas().xywh[0])
            if temp_table.empty == False:  # temp_table is not empty
                # hit the line condition
                temp_table = temp_table[abs(temp_table["xcenter"] - (width / 2)) <= 8]
                current_result = []  # cuurent result update
                current_result = temp_table[["xcenter", "ycenter", "width", "height", "confidence", "name"]].to_numpy()
                # not moving event
                if is_notmoving(previous_result, current_result, distance=7) == False:
                    print(f'current: {current_result}')
                    for i in range(len(current_result)):  # Loop all defect on the Line
                        x = current_result[i][0]
                        y = current_result[i][1]
                        w = current_result[i][2]
                        h = current_result[i][3]
                        All += 1  # count All defect
                        images.append(crop(img, x, y, w, h, All))  # crop the result
                        Total.loc[Total.shape[0]] = current_result[i]  # append row to dataframe
            # update previous to check
            previous_result = current_result

            # Processing time for this frame = Current time – time when previous frame processed
            fps = 1 / (time.time() - prev_frame_time)
            fps = round(fps, 2)
            prev_frame_time = time.time()
            # visualization
            cv.line(img, (int(width / 2), 0), (int(width / 2), height), (0, 0, 255), thickness=3, lineType=cv.LINE_AA)
            cv.putText(img, ('FPS :' + str(fps)),
                       (width - 200, 50), cv.FONT_HERSHEY_PLAIN,
                       2, (0, 255, 0), 2, cv.LINE_AA)
            # cv.imshow('YOLO', np.squeeze(result.render())) # display in backend
            global result_frame
            result_frame = np.squeeze(result.render())  # display in backend
            if saved:
                out.write(np.squeeze(result.render()))
            if cv.waitKey(25) & 0xFF == ord('q'):  # press q to stop inference in backend
                break
        else:
            break
    # end batch of pics
    end_time = time.ctime(time.time())
    cap.release()
    cv.destroyAllWindows()
    # loop in pictures
    print(f'Start : {start_time} , End : {end_time}')
    print(f'ALL Pellet : {total_pellet} ,All Defect : {All}')
    # To count for xlsx
    defect_num = [0 for i in range(len(classes))]
    for i in range(len(defect_num)):
        defect_num[i] = Total[Total["name"] == classes[i]]['name'].count()
    print(f'Total : {Total}')

    # covert output to dataframe
    head = pd.DataFrame({'Start_time': [start_time], 'End_time': [end_time], 'Total_pellet': [total_pellet]})
    # insert for All defect values
    classes.insert(0, 'All Defect')
    defect_num.insert(0, All)
    count = pd.DataFrame(data=[defect_num], columns=classes)
    # # # # Xlsx section
    filepath = "static/output/table_output_" + str(start_time) + ".xlsx"
    filename = "table_output_" + str(start_time) + ".xlsx"
    filepath = filepath.replace(":", "-")
    filename = filename.replace(":", "-")
    global output_path, output_filename
    output_path = filepath
    output_filename = filename
    # print(filepath)
    with pd.ExcelWriter(filepath) as writer:
        head.to_excel(writer, sheet_name='result', index=False)
        count.to_excel(writer, sheet_name='result', index=False, startrow=4)
        Total.to_excel(writer, sheet_name='result', index=False, startrow=8)
    insert_images(dir='static/output/crop', filepath=output_path,
                  classlist=Total.name)  # insert crop images to excel file
    result_frame = 'nopic'
    return True

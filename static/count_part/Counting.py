import cv2
# วาด วงรีคลุมแต่ละ object และนับจำนวน

def is_same(previous, current):  # True => same pellet do not count
    distance, temp = 4, []
    if len(previous) != len(current) or previous == [] or current == []:  # not same
        return False
    for (x1, y1, a1, b1), (x2, y2, a2, b2) in zip(previous, current):
        if abs(x1 - x2) <= distance and abs(y1 - y2) <= distance and abs(a1 - a2 <= 2) and abs(b1 - b2 <= 2):
            temp.append(1)
    return True if len(temp) == len(current) else False


def draw(frame, cnts):
    width, height = 1280, 800
    width = int(2 * width / 3) - int(width / 3)
    frame_pellet = 0
    current = []
    for cnt in cnts:  # each of contours
        area = cv2.contourArea(cnt)
        if area < 400 or area > 10000:
            continue
        ellipse = cv2.fitEllipse(cnt)  # (x,y),(a,b),angle
        # create ellipse boundary
        ellipse = list(ellipse)
        ellipse[1] = list(ellipse[1])
        ellipse[1][0] = ellipse[1][0] * 2
        ellipse[1][1] = ellipse[1][1] * 2
        x = ellipse[0][0]
        y = ellipse[0][1]
        a = ellipse[1][0]
        b = ellipse[1][1]
        # print(f'ellipse : {type(ellipse)}')
        if a / b >= 6.5 or b / a >= 6.5:  # { a , b } axes length
            continue
        if abs((width / 2) - x) <= 5:
            cv2.ellipse(frame, ellipse, (255, 100, 2), 2)
            current.append([x, y, a, b])
        # print(f'current : {current}')
        cv2.line(frame, (int(width / 2), 0), (int(width / 2), height), (0, 0, 255), thickness=3,
                 lineType=cv2.LINE_AA)
    return current, frame

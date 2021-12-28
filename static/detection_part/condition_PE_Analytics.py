def is_notmoving(previous_result,current_result,distance): # True => not moving event False => normal
    count = 0
    if (current_result == [] and previous_result == []) or len(current_result) != len(previous_result):
        return False
    for i in range(len(current_result)):
        # previous
        x1 = previous_result[i][0]
        y1 = previous_result[i][1]
        w1 = previous_result[i][2]
        h1 = previous_result[i][3]
        # current
        x2 = current_result[i][0]
        y2 = current_result[i][1]
        w2= current_result[i][2]
        h2 = current_result[i][3]
        # condition
        if (( abs(x1-x2) <= distance or abs(y1-y2) <= distance ) or  (abs(w1-w2)<1 and abs(h1-h2)<1) ):
            count += 1
    return True if count == len(current_result) else False


import numpy as np

def count_fingers(lmList):
    tipIds = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other 4 fingers
    for id in range(1, 5):
        if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

def is_pinching(lmList):
    x1, y1 = lmList[4][1], lmList[4][2]   # Thumb
    x2, y2 = lmList[8][1], lmList[8][2]   # Index
    distance = np.hypot(x2 - x1, y2 - y1)
    return distance < 40

'''
Gesture Recognition
'''
import cv2
import mediapipe as mp
import time
import math

def get_angle(xFinger, yFinger, xWrist, yWrist):
    xDiff = xFinger - xWrist
    yDiff = yFinger - yWrist
    xBase = 1
    yBase = 0
    try:
        angle = math.degrees(math.acos((xDiff*xBase+yDiff*yBase)/(((xDiff**2+yDiff**2)**0.5)*((xBase**2+yBase**2)**0.5))))
        if yDiff > 0:
            angle = -angle
    except:
        angle = 180
    return round(angle, 2)

def get_length(ax, ay, bx, by):
    length = ((ax - bx)**2 + (ay - by)**2)**0.5
    return length

def get_finger_length(xWrist, yWrist,
                   xThumb, yThumb,
                   xIndexFinger, yIndexFinger,
                   xMiddleFinger, yMiddleFinger,
                   xRingFinger, yRingFinger,
                   xLittleFinger, yLittleFinger):
    ThumbLength = get_length(xWrist, yWrist, xThumb, yThumb)
    IndexLength = get_length(xWrist, yWrist, xIndexFinger, yIndexFinger)
    MiddleLength = get_length(xWrist, yWrist, xMiddleFinger, yMiddleFinger)
    RingLength = get_length(xWrist, yWrist, xRingFinger, yRingFinger)
    LittleLength = get_length(xWrist, yWrist, xLittleFinger, yLittleFinger)
#     avg = (ThumbLength + IndexLength + MiddleLength + RingLength + LittleLength)/5
    FingerLength = [ThumbLength, IndexLength, MiddleLength, RingLength, LittleLength]
    FingerLength = [round(i, 2) for i in FingerLength]
    return FingerLength
    
def get_finger_state(FingerLength:list, Threshold:list):
    FingerState = [False for i in range(len(FingerLength))]
    for i in range(len(FingerLength)):
        if FingerLength[i] > Threshold[i]:
            FingerState[i] = True
        else:
            FingerState[i] = False
    return FingerState

def get_gesture(angle, state):
    if state.count(True) == 5:
        gesture = 'open'
    elif state.count(False) == 5:
        gesture = 'close'
    elif state[1] == True and state.count(True) == 1:
        if -30 < angle < 30:
            gesture = 'left'
        elif -150 < angle < -180 or 150 < angle < 180:
            gesture = 'right'
        elif 60 < angle < 120:
            gesture = 'up'
        elif -120 < angle < -60:
            gesture = 'down'
        else:
            gesture = 'unknown'
    else:
        gesture = 'unknown'
    return gesture
    

# hands variable
STATIC_IMAGE_MODE = False
MAX_NUM_HANDS = 1
MODEL_COMPLEXITY = 1
MIN_DETECTION_CONFIDENCE = 0.1
MIN_TRACKING_CONFIDENCE = 0.3

# get camera
cap = cv2.VideoCapture(0)
# choose mediapipe solution
mpHands = mp.solutions.hands
# set hands variable
hands = mpHands.Hands(STATIC_IMAGE_MODE,
                      MAX_NUM_HANDS,
                      MODEL_COMPLEXITY,
                      MIN_DETECTION_CONFIDENCE,
                      MIN_TRACKING_CONFIDENCE)
mpDraw = mp.solutions.drawing_utils
# draw circle on articulation point (關節點)
handLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)
# draw line between articulation point
handConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=10)
# for FPS calculate
previousTime = 0
currentTime = 0

Threshold = [110, 100, 100, 100, 100]
'''
main code
'''
while True:
    ret, image = cap.read()

    if image is not None:
        # macOS don't need to convert back to RGB
        # imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = hands.process(image)
        # print(result.multi_hand_landmarks)
        # get window size
        imgHeight = image.shape[0]
        imgWidth = image.shape[1]
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)
                for i, lm in enumerate(handLms.landmark):
                    # convert (x, y) percentage to real (x, y) coordinate in window
                    xPos = int(lm.x * imgWidth)
                    yPos = int(lm.y * imgHeight)
#                     finger = (0, 0)
#                     wrist = (0, 0)
                    # put text near the node
                    # cv2.putText(image, str(i), (xPos-25, yPos+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#                     print(i, xPos, yPos)
                    # put circle on thumb
                    
                    if i == 0:
                        cv2.circle(image, (xPos, yPos), 5, (255, 0, 0), cv2.FILLED)
                        xWrist = xPos
                        yWrist = yPos
                    if i == 4:
                        cv2.circle(image, (xPos, yPos), 5, (255, 0, 0), cv2.FILLED)
                        xThumb = xPos
                        yThumb = yPos
                    if i == 8:
                        cv2.circle(image, (xPos, yPos), 5, (255, 0, 0), cv2.FILLED)
                        xIndexFinger = xPos
                        yIndexFinger = yPos
                    if i == 12:
                        cv2.circle(image, (xPos, yPos), 5, (255, 0, 0), cv2.FILLED)
                        xMiddleFinger = xPos
                        yMiddleFinger = yPos
                    if i == 16:
                        cv2.circle(image, (xPos, yPos), 5, (255, 0, 0), cv2.FILLED)
                        xRingFinger = xPos
                        yRingFinger = yPos
                    if i == 20:
                        cv2.circle(image, (xPos, yPos), 5, (255, 0, 0), cv2.FILLED)
                        xLittleFinger = xPos
                        yLittleFinger = yPos
                    
        
            angle = get_angle(xIndexFinger, yIndexFinger, xWrist, yWrist)
#             print(angle)
            FingerLength = get_finger_length(xWrist, yWrist,
                                             xThumb, yThumb,
                                             xIndexFinger, yIndexFinger,
                                             xMiddleFinger, yMiddleFinger,
                                             xRingFinger, yRingFinger,
                                             xLittleFinger, yLittleFinger)
#             print(FingerLength[0], FingerLength[1], FingerLength[2], FingerLength[3], FingerLength[4])
            state = get_finger_state(FingerLength, Threshold)
            print(state)
            gesture = get_gesture(angle, state)
            print(gesture)
        else:
            gesture = 'none'

        # calculate FPS
        currentTime = time.time()
        fps = 1/(currentTime-previousTime)
        previousTime = currentTime
        cv2.putText(image, f"FPS: {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv2.putText(image, f"Gesture: {gesture}", (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2.imshow("image", image)

    # press "q" to exit
    if cv2.waitKey(1) == ord('q'):
        break


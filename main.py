import cv2
import mediapipe as mp
import time

# hands variable
STATIC_IMAGE_MODE = False
MAX_NUM_HANDS = 2
MODEL_COMPLEXITY = 1
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

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
                    # put text near the node
                    # cv2.putText(image, str(i), (xPos-25, yPos+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    print(i, xPos, yPos)
                    # put circle on thumb
                    if i == 4:
                        cv2.circle(image, (xPos, yPos), 20, (255, 0, 0), cv2.FILLED)

        # calculate FPS
        currentTime = time.time()
        fps = 1/(currentTime-previousTime)
        previousTime = currentTime
        cv2.putText(image, f"FPS: {int(fps)}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

        cv2.imshow("image", image)

    # press "q" to exit
    if cv2.waitKey(1) == ord('q'):
        break

'''
Control Speaker by Gesture Recognition
'''
import cv2
import mediapipe as mp
import time
import math
import vlc
import glob
import os 

def set_uri(uri):
    media_player.set_mrl(uri)

# Pause the media player
def pause():
    media_player.pause()

# Resume the media player
def resume():
    media_player.set_pause(0)

# Stop the media player
def stop():
    media_player.stop()

# Release resources
def release():
    return media_player.release()

# Get the current volume (0-100)
def get_volume():
    return media_player.audio_get_volume()

# Set the volume (0-100)
def set_volume(volume):
    return media_player.audio_set_volume(volume)

# Play the next song in the playlist
def next_song(index):
    index += 1
    return index

# Play the previous song in the playlist
def previous_song(index):
    index -= 1
    return index

# Get the current state: Playing, Paused, or Other
def get_state(self):
    state = self.media.get_state()
    if state == vlc.State.Playing:
        return 1
    elif state == vlc.State.Paused:
        return 0
    else:
        return -1

# Calculate the angle between two points
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

# Calculate the distance between two points
def get_length(ax, ay, bx, by):
    length = ((ax - bx)**2 + (ay - by)**2)**0.5
    return length

# Calculate the length of each finger
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
    FingerLength = [ThumbLength, IndexLength, MiddleLength, RingLength, LittleLength]
    FingerLength = [round(i, 2) for i in FingerLength]
    return FingerLength

# Determine if each finger is open or closed
def get_finger_state(FingerLength:list, Threshold:list):
    FingerState = [False for i in range(len(FingerLength))]
    for i in range(len(FingerLength)):
        if FingerLength[i] > Threshold[i]:
            FingerState[i] = True
        else:
            FingerState[i] = False
    return FingerState

# Define a function to get the state of each finger based on its length and threshold
def get_finger_state(FingerLength:list, Threshold:list):
    FingerState = [False for i in range(len(FingerLength))]
    for i in range(len(FingerLength)):
        if FingerLength[i] > Threshold[i]:
            FingerState[i] = True
        else:
            FingerState[i] = False
    return FingerState

# Define a function to get the gesture based on the hand angle and finger state
def get_gesture(angle, state):
    if state.count(True) == 5:
        gesture = 'open'
    elif state.count(False) == 5:
        gesture = 'close'
    elif state[1] == True and state.count(True) == 1:
        if 60 < angle < 120:
            gesture = 'up'
        else:
            gesture = 'unknown'
    elif state[1] == True and state[2] == True and state.count(True) == 2:
        gesture = 'down'
    elif state[0] == True and state[1] == True and state.count(True) == 2:
        if 0 < angle < 90:
            gesture = 'left'
        elif 90 < angle < 180:
            gesture = 'right'
        else:
            gesture = 'unknown'
    else:
        gesture = 'unknown'
    return gesture

# Load music files
base_folder = './music'
song_name = os.listdir(base_folder)
song_name = sorted(song_name)
playlist = glob.glob(base_folder + "/" + "*.mp3")
playlist = sorted(playlist)
playlist_len = len(playlist)
print(f"Total {playlist_len} songs.")

# Initialize music player
inst = vlc.Instance('--no-xlib --quiet ') 
media_player = vlc.MediaPlayer()
idx = 0
media_player.set_media(vlc.Media(playlist[idx]))
media_player.play()
volume = 30
media_player.audio_set_volume(volume)

# Set up hand tracking
STATIC_IMAGE_MODE = False
MAX_NUM_HANDS = 1
MODEL_COMPLEXITY = 1
MIN_DETECTION_CONFIDENCE = 0.1
MIN_TRACKING_CONFIDENCE = 0.3

# Initialize camera and Mediapipe
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands(STATIC_IMAGE_MODE,
                      MAX_NUM_HANDS,
                      MODEL_COMPLEXITY,
                      MIN_DETECTION_CONFIDENCE,
                      MIN_TRACKING_CONFIDENCE)
mpDraw = mp.solutions.drawing_utils
handLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=5)
handConStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=10)

# Initialize some variables
Threshold = [120, 100, 100, 100, 100]
current_gesture_state = 1
previous_gesture_state = 1
music_state_change = False
currentTime = 0
previousTime = 0
startTime = 0
endTime = 0
maintainTime = 0
maintainThreshold = 2

# main loop
while True:
    
    # pause music if hand is closed
    if music_state_change == True and current_gesture_state == 0:
        pause()
    # resume music if hand is open
    elif current_gesture_state == 1:
        resume()
        
    # read from camera
    ret, image = cap.read()

    # if image is not None, process it
    if image is not None:
        # use Mediapipe to get hand landmarks and connections
        result = hands.process(image)

        # get window size
        imgHeight = image.shape[0]
        imgWidth = image.shape[1]
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:
                # draw landmarks and connections on the image
                mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS, handLmsStyle, handConStyle)
                for i, lm in enumerate(handLms.landmark):
                    # convert (x, y) percentage to real (x, y) coordinate in window
                    xPos = int(lm.x * imgWidth)
                    yPos = int(lm.y * imgHeight)
                    
                    # record the positions of important landmarks
                    if i == 0:
                        xWrist = xPos
                        yWrist = yPos
                    if i == 4:
                        xThumb = xPos
                        yThumb = yPos
                    if i == 8:
                        xIndexFinger = xPos
                        yIndexFinger = yPos
                    if i == 12:
                        xMiddleFinger = xPos
                        yMiddleFinger = yPos
                    if i == 16:
                        xRingFinger = xPos
                        yRingFinger = yPos
                    if i == 20:
                        xLittleFinger = xPos
                        yLittleFinger = yPos

            # get angle and finger length    
            angle = get_angle(xIndexFinger, yIndexFinger, xWrist, yWrist)
            FingerLength = get_finger_length(xWrist, yWrist,
                                             xThumb, yThumb,
                                             xIndexFinger, yIndexFinger,
                                             xMiddleFinger, yMiddleFinger,
                                             xRingFinger, yRingFinger,
                                             xLittleFinger, yLittleFinger)
            state = get_finger_state(FingerLength, Threshold)
            gesture = get_gesture(angle, state)
        else:
            gesture = 'none'
        
        # calculate FPS
        currentTime = time.time()
        fps = 1/(currentTime-previousTime)
        previousTime = currentTime
        
#         print(state)
        print(f"FPS: {int(fps)}, Gesture: {gesture}, Volume: {int(volume)}, Index: {idx}, Song name: {song_name[idx]}")
#         print(f"Maintain Time: {maintainTime}")
#         print(f"Start Time: {startTime}")
#         print(f"End Time: {endTime}")
#         
        # Check if fps is greater than 2
        if fps > 2:
            # Check the current gesture
            if gesture == 'open':
                current_gesture_state = 1
            elif gesture == 'close':
                # Start timer
                startTime = time.time()
                # Check if the timer has exceeded the maintain threshold time
                if (startTime - endTime) > maintainThreshold+1:
                    endTime = time.time()
                    maintainTime = 0  
                maintainTime += (startTime - endTime)
                endTime = startTime
                # If maintainTime is greater than the threshold, set gesture state to 0
                if maintainTime > maintainThreshold:
                    current_gesture_state = 0
            elif gesture == 'up':
                # Increase volume by 2
                volume += 2
                # If volume is greater than 100, set volume to 100
                if volume > 100:
                    volume = 100
                    set_volume(volume)
                else:
                    set_volume(volume)
            elif gesture == 'down':
                # Decrease volume by 2
                volume -= 2
                # If volume is less than 0, set volume to 0
                if volume < 0:
                    volume = 0
                    set_volume(volume)
                else:
                    set_volume(volume)
            elif gesture == 'right':
                # Start timer
                startTime = time.time()
                # Check if the timer has exceeded the maintain threshold time
                if (startTime - endTime) > maintainThreshold+1:
                    endTime = time.time()
                    maintainTime = 0
                maintainTime += (startTime - endTime)
                endTime = startTime
                # If maintainTime is greater than the threshold, play the next song
                if maintainTime > maintainThreshold:
                    maintainTime = 0
                    idx = next_song(idx)
                    idx = idx % playlist_len
                    set_uri(playlist[idx])
                    media_player.play()
                continue
            elif gesture == 'left':
                # Start timer
                startTime = time.time()
                # Check if the timer has exceeded the maintain threshold time
                if (startTime - endTime) > maintainThreshold+1:
                    endTime = time.time()
                    maintainTime = 0    
                maintainTime += (startTime - endTime)
                endTime = startTime
                # If maintainTime is greater than the threshold, play the previous song
                if maintainTime > maintainThreshold:
                    maintainTime = 0
                    idx = previous_song(idx)
                    idx = idx % playlist_len
                    set_uri(playlist[idx])
                    media_player.play()
                continue
            
            # Check if previous and current gesture states are equal
            if previous_gesture_state == current_gesture_state:
                music_state_change = False
            # If they are not equal, set music_state_change to True
            elif previous_gesture_state != current_gesture_state:
                music_state_change = True

            # Set the previous gesture state to the current gesture state
            previous_gesture_state = current_gesture_state

                    



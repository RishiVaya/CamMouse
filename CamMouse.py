import cv2 as cv
import mediapipe as mp
import time
import mouse

## - Webcam
camera = cv.VideoCapture(0)
screenh = 1080
screenw = 1920

mpHands = mp.solutions.hands
hands = mpHands.Hands(False, 2, 0.7, 0.7)  ## Max number of hands to identify
mpDraw = mp.solutions.drawing_utils

previoustime = 0
currenttime = 0
prevland = []
login = False

##### Login form
while login == False:
    print("Please enter the 4 digit password!")
    password = input()
    if password == "1111":
        login = True
        print("Welcome to Finger Mouse")
    else:
        print("Incorrect password! Please try again..")


while True:
    isTrue, img = camera.read()
    img = cv.flip(img, 1)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)  ##### COnverts BGR image to rgb
    result = hands.process(imgRGB)
    landmarks = []

    if result.multi_hand_landmarks:  #### If a hand is detected

        ######  -- Used to draw all the hands identified in the image
        for handLms in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        ### -- Used to get locations of all 21 points on the first hand of the image (change index 0 to 1 if want second hand)
        for id, lm in enumerate(result.multi_hand_landmarks[0].landmark):
            height, width, c = img.shape
            xcoor, ycoor = int(lm.x * width), int(lm.y * height)
            landmarks.append([id, xcoor, ycoor])

    ############################################################ Hand mouse controls

    if len(landmarks) != 0 and len(prevland) != 0:
        # print(landmarks[12][1] - landmarks[8][1], landmarks[12][2] - landmarks[8][2])
        if (
            (landmarks[0][2] - landmarks[8][2] > 115)
            and (landmarks[12][2] - landmarks[8][2] > 50)
            and (
                abs(landmarks[8][1] - prevland[8][1]) > 4
                or abs(landmarks[8][2] - prevland[8][2]) > 4
            )
        ):
            pos = mouse.get_position()
            mouse.move(
                pos[0] + (landmarks[8][1] - prevland[8][1]) * 3,
                pos[1] + (landmarks[8][2] - prevland[8][2]) * 3,
            )
            # print((landmarks[8][1] - prevland[8][1]))
            # print(landmarks[8][2] - prevland[8][2])

        if landmarks[0][1] - landmarks[4][1] > 85:
            # print(landmarks[0][1] - landmarks[4][1])
            mouse.click("left")
            print("left click")
            time.sleep(1)

        if landmarks[0][2] - landmarks[20][2] > 100:
            # print(landmarks[0][1] - landmarks[20][1])
            mouse.click("right")
            print("right click")
            time.sleep(1)

        if (
            (landmarks[0][2] - landmarks[8][2] > 115)
            and (landmarks[12][2] - landmarks[8][2] < 10)
            and (landmarks[16][2] - landmarks[12][2] > 50)
        ):
            mouse.wheel(1)  ## scroll up
            # print("scroll up")

        if (
            (landmarks[0][2] - landmarks[8][2] > 115)
            and (landmarks[12][2] - landmarks[8][2] < 10)
            and (landmarks[16][2] - landmarks[12][2] < 10)
        ):
            mouse.wheel(-1)  ## scroll down
            # print("scroll down")

    ##############################################################################################
    ##### -> GEts the fps rate
    # currenttime = time.time()
    # fps = 1 / (currenttime - previoustime)
    # previoustime = currenttime

    #### Prints the fps rate on the screen
    # cv.putText(
    #    img, str(int(fps)), (10, 70), cv.FONT_HERSHEY_COMPLEX, 2, (255, 255, 0), 2
    # )
    cv.imshow("Video", img)
    prevland = landmarks

    if cv.waitKey(20) & 0xFF == ord("d"):
        break

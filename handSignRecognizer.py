#Title: HAND SIGN RECOGNIZER
#Developer: Vishwas Puri
#Purpose: A program that detects out of 8 different types of hand signs to identify, which sign you are making with your hand.

#This program is made using python supported by streamlit.
import streamlit as st
import mediapipe as mp
import cv2
st.set_page_config(layout="wide")
col = st.empty()

#defining mediapipe's inbuilt hand recogignition models
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

from streamlit_webrtc import (
    AudioProcessorBase,
    RTCConfiguration,
    VideoProcessorBase,
    WebRtcMode,
    webrtc_streamer,
)
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal  # type: ignore
import av

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)
st.write("Press start to turn on camera and start making hand signs!")

def handDetector():
    class OpenCVVideoProcessor(VideoProcessorBase):
        def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
            img = frame.to_ndarray(format="bgr24")
            # converting image to RGB
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #analyze hands in the image
            results = hands.process(imgRGB)
            cv2.rectangle(img, pt1=(0,0), pt2=(700,80), color=(0,0,0), thickness= -1)
            #gets the 22 hand points
            if results.multi_hand_landmarks:
                # print(results.multi_hand_landmarks)
                for handLms in results.multi_hand_landmarks:
                    # mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                    lmList = []
                    myHand = results.multi_hand_landmarks[0]
                    for id, lm in enumerate(myHand.landmark):
                        # print(id, lm)
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        # print(id, cx, cy)
                        lmList.append([id, cx, cy])
                    # print(lmList)
                    if len(lmList) != 0:
                        print(lmList)
                        #Checks which symbol does the points orientation illustrate
                        #writes the symbol name on the image
                        if lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][
                            2] and lmList[20][2] > lmList[18][2]:
                            cv2.putText(img, "Pointing Sign", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, 255)

                        elif lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] > lmList[14][
                            2] and lmList[20][2] > lmList[18][2]:
                            cv2.putText(img, "Peace Sign", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, 255)

                        elif lmList[8][2] < lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][
                            2] and lmList[20][2] < lmList[18][2]:
                            cv2.putText(img, "Rock Sign", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, 255)

                        elif lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][
                            2] and lmList[20][2] > lmList[18][2] and lmList[4][2] < lmList[3][2]:
                            cv2.putText(img, "Thumbs Up Sign", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, 255)

                        elif lmList[8][2] > lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] > lmList[14][
                            2] and lmList[20][2] > lmList[18][2]:
                            cv2.putText(img, "Obscene Sign", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, 255)

                        elif lmList[8][2] > lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][
                            2] and lmList[20][2] < lmList[18][2] and lmList[4][2] < lmList[3][2]:
                            cv2.putText(img, "OK Sign", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, 255)

                        elif lmList[8][2] > lmList[6][2] and lmList[12][2] > lmList[10][2] and lmList[16][2] > lmList[14][
                            2] and lmList[20][2] > lmList[18][2]:
                            cv2.putText(img, "Fist Sign", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, 255)

                        elif lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2] and lmList[16][2] < lmList[14][
                            2] and lmList[20][2] < lmList[18][2] and lmList[4][2] <= lmList[3][2]:
                            cv2.putText(img, "High Five Sign", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, 255)

                        else:
                            cv2.putText(img, "Hand Detected!", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, 255)
            else:
                cv2.putText(img, "No Hand Detected!", (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, 255)
            return av.VideoFrame.from_ndarray(img, format="bgr24")

    # setting up streamlit camera configuration
    webrtc_ctx = webrtc_streamer(
        key="opencv-filter",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        video_processor_factory=OpenCVVideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
        video_html_attrs={
            "style": {"margin": "0 auto", "border": "5px yellow solid"},
            "controls": False,
            "autoPlay": True,
        },
    )

    # Info Block
    st.write("If camera doesn't turn on, please ensure that your camera permissions are on!")
    with st.expander("Steps to enable permission"):
        st.write("1. Click the lock button at the top left of the page")
        st.write("2. Slide the camera slider to on")
        st.write("3. Reload your page!")

    st.subheader("Possible Output Signs")
    st.write("Point | Peace | Rock | Thumbs Up | Obscene | OK | Fist | High Five | More to come...")

if __name__ == "__main__":
    handDetector()

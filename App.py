import streamlit as st
import numpy as np
import moviepy
import cv2
from moviepy.editor import VideoFileClip
import time
import tempfile
import os
from streamlit_lottie import st_lottie
import requests

def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def load_lottie_animation():
    lottie_url = "https://assets7.lottiefiles.com/packages/lf20_KhD7qz.json"  
    lottie_json = load_lottie_url(lottie_url)
    if lottie_json:
        st_lottie(lottie_json, speed=1, width=400, height=400, key="animation")
    else:
        st.warning("Unable to load animation.")

def RGB_color_selection(image):
    lower_threshold = np.uint8([200, 200, 200])
    upper_threshold = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(image, lower_threshold, upper_threshold)

    lower_threshold = np.uint8([175, 175, 0])
    upper_threshold = np.uint8([255, 255, 255])
    yellow_mask = cv2.inRange(image, lower_threshold, upper_threshold)

    mask = cv2.bitwise_or(white_mask, yellow_mask)
    return cv2.bitwise_and(image, image, mask=mask)

def convert_hsl(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2HLS)

def HSL_color_selection(image):
    converted_image = convert_hsl(image)

    lower_threshold = np.uint8([0, 200, 0])
    upper_threshold = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(converted_image, lower_threshold, upper_threshold)

    lower_threshold = np.uint8([10, 0, 100])
    upper_threshold = np.uint8([40, 255, 255])
    yellow_mask = cv2.inRange(converted_image, lower_threshold, upper_threshold)

    mask = cv2.bitwise_or(white_mask, yellow_mask)
    return cv2.bitwise_and(image, image, mask=mask)

def gray_scale(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def gaussian_smoothing(image, kernel_size=13):
    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

def canny_detector(image, low_threshold=50, high_threshold=150):
    return cv2.Canny(image, low_threshold, high_threshold)

def region_selection(image):
    mask = np.zeros_like(image)
    rows, cols = image.shape[:2]
    bottom_left = [cols * 0.1, rows * 0.95]
    top_left = [cols * 0.4, rows * 0.6]
    bottom_right = [cols * 0.9, rows * 0.95]
    top_right = [cols * 0.6, rows * 0.6]
    vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)
    cv2.fillPoly(mask, vertices, 255)
    return cv2.bitwise_and(image, mask)

def hough_transform(image):
    rho = 1
    theta = np.pi / 180
    threshold = 20
    min_line_length = 20
    max_line_gap = 300
    return cv2.HoughLinesP(image, rho, theta, threshold, minLineLength=min_line_length, maxLineGap=max_line_gap)

def draw_lane_lines(image, lines, color=[255, 0, 0], thickness=12):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), color, thickness)
    return cv2.addWeighted(image, 1.0, line_image, 1.0, 0.0)

def frame_processor(image):
    color_select = HSL_color_selection(image)
    gray = gray_scale(color_select)
    smooth = gaussian_smoothing(gray)
    edges = canny_detector(smooth)
    region = region_selection(edges)
    hough = hough_transform(region)
    return draw_lane_lines(image, hough)

def process_video(input_video_path, output_video_path, progress_bar):
    try:
        input_video = VideoFileClip(input_video_path)
        processed = input_video.fl_image(frame_processor)
        processed.write_videofile(output_video_path, codec="libx264", audio=False)
        
        progress_bar.progress(100)
    except Exception as e:
        st.error(f"Error during video processing: {e}")

st.title("Lane Detection App")
st.sidebar.header("Upload a Video")
st.sidebar.image("https://cdn.iconscout.com/icon/premium/png-256-thumb/lane-departure-warning-1600566-1356897.png", width=100)


uploaded_video = st.sidebar.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

if uploaded_video:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_input_file:
        temp_input_file.write(uploaded_video.read())
        input_video_path = temp_input_file.name

    output_video_path = os.path.join(tempfile.gettempdir(), "processed_video.mp4")

    progress_bar = st.sidebar.progress(0)

    st.info("Processing your video... Please wait.")

    process_video(input_video_path, output_video_path, progress_bar)
    
    time.sleep(2) 

    st.video(output_video_path)

    with open(output_video_path, "rb") as video_file:
        st.download_button(
            label="Download Processed Video",
            data=video_file,
            file_name="processed_video.mp4",
            mime="video/mp4"
        )

    st.sidebar.button("Upload a New Video", key="upload_new_video")

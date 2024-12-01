# Lane Detection using OpenCV and Streamlit

## 📌 Project Overview

This project implements a Lane Detection system using OpenCV and Streamlit. It processes videos to detect lane lines, a critical feature for applications like self-driving cars and advanced driver assistance systems (ADAS). The system uses computer vision techniques to identify and highlight lane boundaries in real-time video footage.

## System Requirements

To run this project, ensure your system meets the following requirements:

- **Operating System**: Windows/Linux/MacOS
- **Python Version**: 3.8 or higher
- **RAM**: 4GB or higher
- **Storage**: At least 500MB of free space

## Extension Requirements

The project requires the following Python libraries:

- **Streamlit**: For the web-based user interface
- **OpenCV**: For image processing
- **MoviePy**: For video editing and processing
- **Numpy**: For numerical operations
- **Streamlit-Lottie**: For adding animations
- **Requests**: For fetching Lottie animations

You can install the dependencies using the following command:

```bash
pip install streamlit opencv-python moviepy numpy streamlit-lottie requests
```

## Utility Requirements

- **Web Browser**: Chrome, Firefox, or any modern web browser for running the Streamlit app.
- **Code Editor**: Visual Studio Code or any text editor for editing code.

## How to Run the Project

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/lane-detection.git
   cd lane-detection
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app**:
   ```bash
   streamlit run app.py
   ```

4. **Upload a video** through the Streamlit interface, and the system will process it to detect lane lines.

## Concepts Used

The following concepts are utilized in this project:

1. **Color Selection**: Filters specific color ranges to identify lane lines.
2. **Grayscale Conversion**: Simplifies image data for processing.
3. **Gaussian Smoothing**: Reduces noise in the image.
4. **Canny Edge Detection**: Detects edges in the image.
5. **Region of Interest Selection**: Focuses on the area where lanes are expected.
6. **Hough Transform**: Identifies lane lines in the edge-detected image.
7. **Weighted Image Overlay**: Combines the detected lines with the original frame.

## Results

- The system accurately detects and highlights lane lines in uploaded video footage.
- The processed video with detected lanes can be downloaded for further use.
- Here’s an example of the result:

  **Before Processing:**
  ![Before Processing](examples/example-before.jpg)

  **After Processing:**
  ![After Processing](examples/example-after.jpg)

## Future Improvements

- Enhance lane detection under varying lighting conditions.
- Improve performance for real-time video streams.
- Integrate additional features like obstacle detection.

---

Feel free to customize this README to match your specific project setup and repository.

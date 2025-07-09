from flask import Flask, Response
import cv2

app = Flask(__name__)

# Replace with a real file path if needed
cap = cv2.VideoCapture("sample1.mp4")  # Use full path if needed

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video
            continue

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def home():
    return "<h2>Video Feed Test</h2><img src='/video_feed'/>"

if __name__ == '__main__':
    app.run(debug=True)

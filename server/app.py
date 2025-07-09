# from flask import Flask, Response, jsonify
# from ultralytics import YOLO
# import cv2
# from flask_cors import CORS
# import threading
# import time

# app = Flask(__name__)
# CORS(app)  # ✅ Moved here after app = Flask()

# model = YOLO("yolov8n.pt")
# # cap = cv2.VideoCapture(0)  # Use 0 for laptop webcam
# # cap = cv2.VideoCapture(cv2.CAP_AVFOUNDATION)
# # cap = cv2.VideoCapture("sample.mp4")
# cap = cv2.VideoCapture("/Users/hemanthreddy/Desktop/personal/cctv-analyzer-app/server/sample.mp4")


# live_counts = {
#     "person": 0,
#     "car": 0,
#     "bike": 0
# }

# def gen_frames():
#     while True:
#         success, frame = cap.read()
#         print("Frame success:", success)
#         if not success:
#             break

#         results = model(frame)[0]

#         # Reset counts every frame
#         counts = {"person": 0, "car": 0, "bike": 0}

#         for box in results.boxes:
#             cls = int(box.cls[0])
#             label = model.names[cls]

#             if label == "person":
#                 counts["person"] += 1
#             elif label in ["car", "bus", "truck"]:
#                 counts["car"] += 1
#             elif label in ["motorcycle", "bicycle"]:
#                 counts["bike"] += 1

#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             conf = float(box.conf[0])
#             cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
#             cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1-10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

#         global live_counts
#         live_counts = counts

#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/counts')
# def get_counts():
#     return jsonify(live_counts)

# @app.route('/ping')
# def ping():
#     return jsonify({"status": "online"})

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, Response
# import cv2

# app = Flask(__name__)
# cap = cv2.VideoCapture("sample.mp4")

# def gen():
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # loop video
#             continue
#         ret, jpeg = cv2.imencode('.jpg', frame)
#         frame = jpeg.tobytes()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, Response, jsonify
from ultralytics import YOLO
import cv2

app = Flask(__name__)

model = YOLO("yolov8n.pt")  # ✅ Make sure this file is in the same folder
cap = cv2.VideoCapture("sample1.mp4")  # Use your test video
# cap = cv2.VideoCapture("rtsp://<ip-camera-url>") For Real-Time CCTV

success, frame = cap.read()

if success:
    print("✅ Video file is readable and frame loaded!")
else:
    print("❌ Video file can't be read! Check path or format.")


live_counts = {"person": 0, "car": 0, "bike": 0}

def gen_frames():
    global live_counts
    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # loop the video
            continue

        results = model(frame)[0]

        # Reset counts
        counts = {"person": 0, "car": 0, "bike": 0}

        for box in results.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            if label == "person":
                counts["person"] += 1
            elif label in ["car", "bus", "truck"]:
                counts["car"] += 1
            elif label in ["bicycle", "motorcycle"]:
                counts["bike"] += 1

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
            cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

        live_counts = counts

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def home():
    return "<h2>YOLO Stream</h2><img src='/video_feed' /><p><a href='/counts'>Counts</a></p>"

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/counts')
def counts():
    return jsonify(live_counts)

if __name__ == '__main__':
    app.run(debug=True)

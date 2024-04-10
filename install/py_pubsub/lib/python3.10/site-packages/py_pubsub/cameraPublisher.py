import cv2
import rclpy
from sensor_msgs.msg import Image
from std_msgs.msg import String  # Импортируем String сообщение
from rclpy.node import Node
from cv_bridge import CvBridge
from ultralytics import YOLO

# YOLO model
model = YOLO("yolo-Weights/yolov8n.pt")

# OBJECT CLASS NAMES
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "ball", "skis", "snowboard", "ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "ball", "sandwich", "ball", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

class PublisherNodeClass(Node):

    def __init__(self):
        super().__init__('publisher_node')
        self.cameraDeviceNumber = 0
        self.camera = cv2.VideoCapture(self.cameraDeviceNumber)
        self.bridgeObject = CvBridge()
        self.publisher = self.create_publisher(Image, 'topic_camera_image', 10)
        self.color_publisher = self.create_publisher(String, 'topic_object_color', 10)
        self.timer = self.create_timer(0.1, self.timer_callbackFunction)

    def timer_callbackFunction(self):
        success, frame = self.camera.read()
        #frame = cv2.resize(frame, (820,640), interpolation=cv2.INTER_CUBIC)#820,640#480, 640
        results = model(frame, stream=True)
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        cx = 0
        cy = 0
        color = "Undefined"
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cls = int(box.cls[0])
                class_name = classNames[cls]
                if class_name == "ball":
                    center_diagonal_x = (x1 + x2) // 2
                    center_diagonal_y = (y1 + y2) // 2
                    text_size = cv2.getTextSize(color, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
                    text_x = center_diagonal_x - text_size[0] // 2
                    text_y = center_diagonal_y - text_size[1] // 2
                    cy = text_y + 10
                    cx = text_x + 35
                    cv2.circle(frame, (cx, cy), 5, (25, 25, 25), 3)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    hue_value = hsv_frame[cy, cx, 0]
                    if 0 <= hue_value < 5 or 170 <= hue_value <= 179:
                        color = "RED"
                        print ("RED")
                    elif 5 <= hue_value < 22:
                        color = "ORANGE"
                        print("ORANGE")
                    elif 22 <= hue_value < 33:
                        color = "YELLOW"
                        print("YELLOW")
                    elif 33 <= hue_value < 78:
                        color = "GREEN"
                        print("GREEN")
                    elif 78 <= hue_value < 131:
                        color = "BLUE"
                        print("BLUE")

                color_msg = String()
                color_msg.data = color
                self.color_publisher.publish(color_msg)
                org = (x1, y1 - 25)
                cv2.putText(frame, color, org, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                    
        #cv2.imshow('Webcam', frame)

def main (args=None):
   rclpy.init(args=args)
   publisherObject = PublisherNodeClass()
   rclpy.spin(publisherObject)
   publisherObject.destroy_node()
   rclpy.shutdown()

if __name__ == '__main__':
   main()


from ultralytics import YOLO
import cv2
import time

# START THE WEBCAM
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

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
while True:
    
    if cv2.waitKey(100) == ord('q'):#pause of cykle in real time (waitKey)
     #time.sleep(0.5)
     break    

    success, img = cap.read()
    results = model(img, stream=True)

    hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    #VARIABLES FOR CENTER
    cx = 0
    cy = 0
    color = "Undefined"

    # COORDINATES   
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # BOUNDING RECTANGLE
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # переводимо у цілі значення

            #CLASS NAME VALIDATION (class name)
            cls = int(box.cls[0])
            class_name = classNames[cls]

            #IF THE NAME OF OBJECT IS - "ball"
            if class_name == "ball":

               #CALCULATION OF THE COORDINATESOF THE CENTER OF THE DIAGONAL 
               center_diagonal_x = (x1 + x2) // 2
               center_diagonal_y = (y1 + y2) // 2

               #CALCULATE THE SIZE OF TEXT
               text_size = cv2.getTextSize(color, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
               text_x = center_diagonal_x - text_size[0] // 2
               text_y = center_diagonal_y - text_size[1] // 2
               cy = text_y+10
               cx = text_x+35

               #DRAW THE CENTER POINT
               cv2.circle(img, (cx, cy), 5, (25, 25, 25), 3)

               # DRAW THE WINDOW
               cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)  # GREEN COLOR (window)
               
               hue_value = hsv_frame[cy, cx, 0]
               
               if 0 <= hue_value < 5 or 170 <= hue_value <= 179:
                 color = "RED"
                 print("RED")
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
                                   
                # WE DISPLAY THE COLOR ON THE IMAGE
               org = (x1, y1 - 25)  # PLACING THE TEXT ABOVE THE FRAME
               cv2.putText(img, color, org, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)  
    cv2.imshow('Webcam', img)

cap.release()
cv2.destroyAllWindows()

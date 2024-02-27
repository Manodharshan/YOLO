import numpy as np
import time
import cv2
import pyttsx3

label_path = "coco.names"
yolo_config_path = "yolov2.cfg"
yolo_weight_path = "yolov2.weights"
base_confidence = 0.5

threshold = 0.6


# engine = pyttsx3.init()


# def speak(text):
    # engine.say(text)
    # engine.runAndWait()


LABELS = open(label_path).read().strip().split('\n')

net = cv2.dnn.readNetFromDarknet(
    yolo_config_path, yolo_weight_path
        )

np.random.seed(42)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")

cap = cv2.VideoCapture(0)


ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
frame_counter = 0

detect_per = 40

boxes = []
confidences = []
class_ids = []
while True:
    frame_counter += 1
    ok, img = cap.read()

    start = time.time()
    if (frame_counter % detect_per) == 0:
        H, W = img.shape[:2]
        blob = cv2.dnn.blobFromImage(
                img, 1 / 255, (416, 416), swapRB=True, crop=True)
        boxes = []
        confidences = []
        class_ids = []

        net.setInput(blob)

        layer_output = net.forward(ln)

        end = time.time()

        print("[INFO] Predicted in", end-start)

        frame_counter = 0
        for out in layer_output:
            for detection in out:

                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > base_confidence:

                    box = detection[:4] * np.array([W, H, H, W])
                    (cx, cy, w, h) = box.astype("int")

                    print("Found", LABELS[class_id], "At", (cx, cy))

                    boxes.append(
                            (int(cx-(w/2)), int(cy-(h/2)), int(w), int(h))
                            )
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, base_confidence, threshold)

    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = [int(c) for c in COLORS[class_ids[i]]]

            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)

            text = "{}: {:.4f}".format(LABELS[class_ids[i]], confidences[i])

            # speak(f"Found {LABELS[class_ids[i]]} at left")
            cv2.putText(
                img, text, (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    end = time.time()

    print("[INFO] Loop in", end-start)
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

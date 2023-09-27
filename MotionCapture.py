import cv2
import numpy as np
from GiftWrapping import GiftWrap  # Replace with your convex hull algorithm

def detect_hand(frame, net):
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (127.5, 127.5, 127.5), swapRB=True, crop=False)
    net.setInput(blob)
    detections = net.forward()
    
    # Initialize lists for hand bounding boxes and hand points
    hand_boxes = []
    hand_points = []

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Confidence threshold
            class_id = int(detections[0, 0, i, 1])
            if class_id == 0:  # Class 0 represents hands in the pre-trained model
                box = detections[0, 0, i, 3:7] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                (startX, startY, endX, endY) = box.astype("int")
                hand_boxes.append((startX, startY, endX, endY))
                
                # Extract hand region from the frame
                hand = frame[startY:endY, startX:endX]
                hand_points.extend(get_hand_contour(hand))

    return hand_boxes, hand_points

def get_hand_contour(hand):
    # Preprocess hand region (grayscale, thresholding, etc.)
    gray = cv2.cvtColor(hand, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (assuming it's the hand)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        return [tuple(point[0]) for point in largest_contour]
    else:
        return []

def main():
    # Load the pre-trained hand detection model
    net = cv2.dnn.readNet('hand_detection_model.pb', 'hand_detection_model.pbtxt')

    # Initialize the camera (usually, 0 is the default camera)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            break

        # Detect hands and get hand contour points
        hand_boxes, hand_points = detect_hand(frame, net)

        # Draw bounding boxes around detected hands
        for (startX, startY, endX, endY) in hand_boxes:
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

        # Compute the convex hull of the hand contour points
        convex_hull = GiftWrap(points=hand_points)

        # Draw the convex hull on the frame
        cv2.drawContours(frame, [convex_hull], 0, (0, 0, 255), 2)

        # Display the frame with hand detection and convex hull
        cv2.imshow('Motion Capture with Hand Detection', frame)

        # Exit the loop when the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

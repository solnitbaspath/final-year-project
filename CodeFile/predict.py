import cv2
import torch
import numpy as np
# Load the model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp/weights/best.pt', force_reload=True)

# Set webcam input
cam = cv2.VideoCapture(0)

while True:
    # Read frames
    ret, img = cam.read()

    # Perform object detection
    results = model(img)

    # Display predictions
    #results.show()
    cv2.imshow("Output", np.squeeze(results.render()))

    # Press 'q' or 'Esc' to quit
    if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
        break

# Close the camera
cam.release()
cv2.destroyAllWindows()
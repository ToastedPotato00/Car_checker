from imageai.Detection import ObjectDetection
import os
import cv2
SAVE_FOLDER = "saved_images"
execution_path = os.getcwd()
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "yolov3.pt"))
detector.loadModel()

def image_detection(input_image_path):
    """
    Modified function that takes the image path as parameter
    """
    try:
        detections = detector.detectObjectsFromImage(
            input_image=input_image_path, 
            minimum_percentage_probability=30
        )
        
        car_found = False
        for eachObject in detections:
            if eachObject['name'] == 'car':
                coordinate = eachObject["box_points"]
                img = cv2.imread(input_image_path)
                
                if img is not None:
                    # Extract the car region
                    img_cropped = img[coordinate[1]:coordinate[3], coordinate[0]:coordinate[2]]
                    
                    # Save the detected car
                    output_path = os.path.join(SAVE_FOLDER, "detected_car.jpg")
                    cv2.imwrite(output_path, img_cropped)
                    car_found = True
                    print(f"Car detected and saved to {output_path}")
                    break
                else:
                    print("Error: Could not load image")
                    
        return car_found
        
    except Exception as e:
        print(f"Error in car detection: {e}")
        return False

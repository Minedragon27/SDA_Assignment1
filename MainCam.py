import cv2 #import cv2 library
import numpy as np # import numpy library
# Blank line
class Camera: # create Class Camera
    def __init__(self, camera_address = 0): # Initialize the class 
        self.__camera_address = camera_address # Set Camera Address
        self.vid_capture = cv2.VideoCapture(camera_address, cv2.CAP_DSHOW) # Capture Live Feed of the camera
# Blank line
        if not self.vid_capture.isOpened(): # If camera is not available 
            raise Exception("Error opening the camera") # Error opening camera
# Blank line
# *****Resolution*****
    def setResolution(self, width, height): # Method to set the resolution
# Blank line
        self.vid_capture.set(cv2.CAP_PROP_FRAME_WIDTH, width) # Set Width of the resolution
        self.vid_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height) # Set Height of the resolution
# Blank line 
# *****Video Live Feed*****
    def getImage(self, crop_x1, crop_y1, crop_x2, crop_y2): # Method to get and crop the live feed
# Blank line
        ret, frame = self.vid_capture.read() # Read the camera feed
        if ret: # If statement to crop the image
            cropped_image = frame[crop_y1:crop_y2, crop_x1:crop_x2] # crop frame 
            return cropped_image # Return Cropped image to use in the other methods
        else: # Else Statement if there is no camera feed
            return None # Return None if image is unable to be cropped
# Blank Line        
# *****Shapes Info***** 
    def getShapes(self, frame): # Method to extract information of the shapes
# *****Apply Filters*****
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Turn frame into grayscale
        blur_frame = cv2.GaussianBlur(gray_frame, (5, 5), 0) # Gaussion Blur Filter the frame
        edges = cv2.Canny(blur_frame, threshold1=50, threshold2=150) # Canny Edge Detection to find the edges
        kernel = np.ones((5, 5), np.uint8) # Kernel Matrix for image processing operations like dilation
        edges = cv2.dilate(edges, kernel, iterations=1) # Apply Dialation on the image to bridge the gaps in the contour, thicken line and fill small holes
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Find the contours in the camera feed 
        object_count = len(contours) # Count the number of contours in the feed
        print(f"Objects Detected: {object_count}") # Print the number of objects in the terminal
# Blank Line
        shapes_info_list = [] # List to store information of the shapes
# Blank Line
        for contour in contours: # for loop for noise reduction
# *****Noise Reduction*****
            area = cv2.contourArea(contour) # Find the area of the contours
            if area < 500: # If statement to ignore small contours
                continue # Continue after ignoring small contours
            epsilon = 0.03 * cv2.arcLength(contour, True) # Simplify the value of the contours
            approx = cv2.approxPolyDP(contour, epsilon, True) # Approximate the number of contours
# Blank Line
# *****Smallest Bounding Rect*****
            min_area_rect = cv2.minAreaRect(contour) # Draw the smallest possible bounding rect
            box_points = cv2.boxPoints(min_area_rect) # Find the corners of the bounding rect
            box_points = np.int32(box_points) # Convert Floats to int32 datatype
# Blank Line
# *****Detect Triangle*****
            if len(approx) == 3: # If statement to detect shapes
                shape_name = "Triangle" # Give shape name Triangle if the 3 edges are detected
# Blank Line
# *****Largest Side Bounding Rect and Position of the Vertex for Triangle*****
                side_lengths = [] # Array to store side lengths of the bounding rect
                for i in range(4): # For loop to differentiate sides of the bounding rect
                    next_i = (i + 1) % 4 # 
                    side_length = np.linalg.norm(box_points[i] - box_points[next_i])
                    side_lengths.append(side_length)
# Blank Line
                longest_side_index_1 = np.argmax(side_lengths)
                longest_side_index_2 = (longest_side_index_1 + 2) % 4 
# Blank Line
                pt1 = box_points[longest_side_index_1]
                pt2 = box_points[(longest_side_index_1 + 1) % 4]
                midpoint_1 = ((pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2)
# Blank Line
                pt3 = box_points[longest_side_index_2]
                pt4 = box_points[(longest_side_index_2 + 1) % 4]
                midpoint_2 = ((pt3[0] + pt4[0]) // 2, (pt3[1] + pt4[1]) // 2)
# Blank Line
                distances_1 = [np.linalg.norm(midpoint_1 - vertex[0]) for vertex in approx]
                distances_2 = [np.linalg.norm(midpoint_2 - vertex[0]) for vertex in approx]
# Blank Line
                if min(distances_1) < min(distances_2):
                    position = (int(midpoint_1[0]), int(midpoint_1[1]))  
                else:
                    position = (int(midpoint_2[0]), int(midpoint_2[1])) 
# Blank Line
# *****Detect Square*****
            elif len(approx) == 4:
                shape_name = "Square"
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w) / h
                if 0.95 <= aspect_ratio <= 1.05:
                    shape_name = "Square"
                else:
                    shape_name = "Rectangle"
                position = (int(box_points[box_points[:, 0].argmin()][0]), int(box_points[box_points[:, 0].argmin()][1])) 
# Blank Line
# *****Detect Circle*****
            else:
                perimeter = cv2.arcLength(contour, True)
                area = cv2.contourArea(contour)
                circularity = 4 * np.pi * (area / (perimeter ** 2))
                if 0.7 <= circularity <= 1.2:
                    shape_name = "Circle"
                    position = (int(box_points[box_points[:, 0].argmin()][0]), int(box_points[box_points[:, 0].argmin()][1])) 
                else:
                    shape_name = "Polygon"
                    position = (int(contour[contour[:, :, 0].argmin()][0][0]), int(contour[contour[:, :, 0].argmin()][0][1]))  
# Blank Line
# *****Draw Bounding Rect*****
            cv2.drawContours(frame, [box_points], 0, (0, 255, 255), 2)
# Blank Line
# *****Rotation*****
            width, height = min_area_rect[1]
            rotation_relative_to_longest_side = min_area_rect[2]
# Blank Line
# *****Binary mask*****
            mask = np.zeros_like(frame[:, :, 0])
            cv2.drawContours(mask, [contour], -1, 255, -1)
            mean_color_bgr = cv2.mean(frame, mask=mask)[:3]
            mean_color_rgb = (int(mean_color_bgr[2]), int(mean_color_bgr[1]), int(mean_color_bgr[0]))
# Blank Line
# *****Shapes List*****
            shape_info = {
                'type': shape_name,
                'position': position,
                'color': mean_color_rgb,
                'rotation': round(rotation_relative_to_longest_side, 2),
                'longest_side_length': round(max(width, height), 2)
            }
            shapes_info_list.append(shape_info)
# Blank Line
# *****Centroid(Inaccurate)*****
            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
            else:
                cx, cy = 0, 0
# Blank Line
# *****Draw Position and Centroid*****
            cv2.circle(frame, position, 5, (0, 0, 255), -1)
            cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
# Blank Line
        return frame, shapes_info_list, object_count
# Blank Line
# *****Release camera*****
    def release_camera(self):
        self.vid_capture.release()
        cv2.destroyAllWindows()
# Blank Line
# *****Cropping Dimensions(Changes with Resolution)*****
crop_x1, crop_y1, crop_x2, crop_y2 = 410, 255, 725, 575
# Blank Line
# *****Initialize Camera*****
camera = Camera()
# Blank Line
# *****Set Resolution*****
camera.setResolution(1280, 720)
# Blank Line
# *****Detection Loop*****
while True:
    frame = camera.getImage(crop_x1, crop_y1, crop_x2, crop_y2)
    if frame is None:
        break
# Blank Line
    processed_frame, shapes_info_list, object_count = camera.getShapes(frame)
# Blank Line
    cv2.imshow('Shape Frame', processed_frame)
# Blank Line
    print("Shapes Infor:", shapes_info_list)
# Blank Line
    if cv2.waitKey(20) == ord('q'):
        break
# Blank Line
camera.release_camera()
# End of the code
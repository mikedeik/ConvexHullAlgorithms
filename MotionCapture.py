import cv2
import numpy as np
from QuickHull import getNpArrayFromCH  # Replace with your convex hull algorithm

def find_animal(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to the HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the color range of the animal (adjust as needed)
    lower_color = np.array([5, 50, 50])  # Lower bound for orange color
    upper_color = np.array([15, 255, 255])  # Upper bound for orange color

    # Create a mask for the specified color range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour (assuming it represents the animal)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        print(len(largest_contour))

        # Compute the convex hull of the animal contour
        convex_hull = getNpArrayFromCH(points=[tuple(point[0]) for point in largest_contour])

        # Create a binary mask for the animal
        animal_mask = np.zeros_like(image)
        
        cv2.fillPoly(animal_mask, [convex_hull], (255, 255, 255))

        # Crop the animal region from the original image
        cropped_animal = cv2.bitwise_and(image, animal_mask)

        return cropped_animal

    else:
        return None

def main():
    image_path = 'test2.jpeg'  # Replace with the path to your animal image
    cropped_animal = find_animal(image_path)

    if cropped_animal is not None:
        # Save the cropped animal region as a new image file
        output_filename = 'newfile.jpeg'
        cv2.imwrite(output_filename, cropped_animal)
        print(f"Saved the cropped animal as '{output_filename}'")
    else:
        print("No animal contour found in the image.")

if __name__ == '__main__':
    main()

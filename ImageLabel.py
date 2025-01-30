import os
from google.cloud import vision
from google.cloud.vision_v1 import types

# Set the path to your service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "project1-446502-49fc79d63805.json"

# Initialize the Vision API client
client = vision.ImageAnnotatorClient()

# Path to the main folder containing subfolders with images
main_folder_path = "images"

# Process each image in the folder structure
for subdir, _, files in os.walk(main_folder_path):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            image_path = os.path.join(subdir, file)
            
            # Read the image file
            with open(image_path, 'rb') as image_file:
                content = image_file.read()
                image = types.Image(content=content)
            
            # Call the Vision API to get labels
            response = client.label_detection(image=image)
            labels = response.label_annotations
            
            # Prepare the output
            output_text = f"Image: {file}\n"
            output_text += "-" * 40 + "\n"
            for label in labels:
                output_text += (
                    f"Description: {label.description}\n"
                    f"Score: {label.score:.2f}\n"
                    f"Topicality: {label.topicality:.2f}\n"
                )
                output_text+=f"-" * 20 + "\n"
            
            # Save results as a text file in the same folder
            output_file_path = os.path.join(subdir, os.path.splitext(file)[0] + ".txt")
            with open(output_file_path, 'w') as output_file:
                output_file.write(output_text)
            
            print(f"Processed and saved labels for {image_path}")
            # exit()

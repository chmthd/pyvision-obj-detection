import os
import json

annotation_file = 'D:/Projects/Coding/deepvision/datasets/coco/annotations/instances_train2017.json'
images_dir = 'D:/Projects/Coding/deepvision/datasets/coco/train2017'

with open(annotation_file, 'r') as f:
    data = json.load(f)

missing_files = []
for image_info in data['images']:
    image_file = os.path.join(images_dir, image_info['file_name'])
    if not os.path.exists(image_file):
        missing_files.append(image_info['file_name'])

if missing_files:
    print(f"Missing files: {missing_files}")
else:
    print("All files are present.")

import os
import json
from tqdm import tqdm

# Define paths for COCO annotations and images
annotation_paths = {
    'train': 'D:/Projects/Coding/deepvision/datasets/coco/annotations/instances_train2017.json',
    'val': 'D:/Projects/Coding/deepvision/datasets/coco/annotations/instances_val2017.json'
}
image_dirs = {
    'train': 'D:/Projects/Coding/deepvision/datasets/coco/train2017',
    'val': 'D:/Projects/Coding/deepvision/datasets/coco/val2017'
}
output_labels_dirs = {
    'train': 'D:/Projects/Coding/deepvision/datasets/coco/labels/train2017',
    'val': 'D:/Projects/Coding/deepvision/datasets/coco/labels/val2017'
}

for output_dir in output_labels_dirs.values():
    os.makedirs(output_dir, exist_ok=True)

# Function to convert COCO bbox to YOLO bbox format
def convert_bbox(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[2] / 2.0) * dw
    y = (box[1] + box[3] / 2.0) * dh
    w = box[2] * dw
    h = box[3] * dh
    return (x, y, w, h)

# Process annotations for both training and validation phases
for phase in ['train', 'val']:
    print(f"Processing {phase} annotations...")

    with open(annotation_paths[phase], 'r') as f:
        coco_data = json.load(f)
    
    for image in tqdm(coco_data['images']):
        image_id = image['id']
        file_name = image['file_name']
        width = image['width']
        height = image['height']

        annotations = [a for a in coco_data['annotations'] if a['image_id'] == image_id]
        if not annotations:
            print(f"No annotations found for image {file_name}")
            continue

        label_file_path = os.path.join(output_labels_dirs[phase], os.path.splitext(file_name)[0] + '.txt')
        
        with open(label_file_path, 'w') as label_file:
            for ann in annotations:
                category_id = ann['category_id'] - 1  # YOLO class indices start from 0
                bbox = convert_bbox((width, height), ann['bbox'])
                label_file.write(f"{category_id} {' '.join(map(str, bbox))}\n")
        
        print(f"Processed {file_name} with {len(annotations)} annotations")

print("Conversion completed.")

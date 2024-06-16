import os
import json
from tqdm import tqdm
from pycocotools.coco import COCO
from pathlib import Path

def create_yolo_annotation(bbox, image_width, image_height, category_id):
    x_min, y_min, width, height = bbox
    x_center = x_min + width / 2
    y_center = y_min + height / 2

    x_center /= image_width
    y_center /= image_height
    width /= image_width
    height /= image_height

    return f"{category_id} {x_center} {y_center} {width} {height}"

def convert_coco_to_yolo(coco_annotation_file, image_dir, output_dir):
    coco = COCO(coco_annotation_file)
    image_ids = coco.getImgIds()
    category_ids = coco.getCatIds()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for image_id in tqdm(image_ids, desc=f'Processing {os.path.basename(image_dir)}'):
        image_info = coco.loadImgs(image_id)[0]
        annotation_ids = coco.getAnnIds(imgIds=image_id, catIds=category_ids, iscrowd=None)
        annots = coco.loadAnns(annotation_ids)

        label_filename = os.path.join(output_dir, f"{Path(image_info['file_name']).stem}.txt")
        with open(label_filename, 'w') as label_file:
            for annotation in annots:
                category_id = annotation['category_id'] - 1 
                bbox = annotation['bbox']
                yolo_annotation = create_yolo_annotation(bbox, image_info['width'], image_info['height'], category_id)
                label_file.write(yolo_annotation + '\n')

# Convert train2017
coco_annotation_file = 'D:/Projects/Coding/deepvision/datasets/coco/annotations/instances_train2017.json'
image_dir = 'D:/Projects/Coding/deepvision/datasets/coco/train2017'
output_dir = 'D:/Projects/Coding/deepvision/datasets/coco/labels/train2017'
convert_coco_to_yolo(coco_annotation_file, image_dir, output_dir)

# Convert val2017
coco_annotation_file = 'D:/Projects/Coding/deepvision/datasets/coco/annotations/instances_val2017.json'
image_dir = 'D:/Projects/Coding/deepvision/datasets/coco/val2017'
output_dir = 'D:/Projects/Coding/deepvision/datasets/coco/labels/val2017'
convert_coco_to_yolo(coco_annotation_file, image_dir, output_dir)

import os
import cv2

image_dir = 'D:/Projects/Coding/deepvision/datasets/coco/train2017'
label_dir = 'D:/Projects/Coding/deepvision/datasets/coco/labels/train2017'

def visualize_annotations(image_dir, label_dir, num_images=5):
    for idx, image_file in enumerate(os.listdir(image_dir)):
        if idx >= num_images:
            break
        
        image_path = os.path.join(image_dir, image_file)
        label_path = os.path.join(label_dir, os.path.splitext(image_file)[0] + '.txt')

        # Load image
        image = cv2.imread(image_path)
        height, width, _ = image.shape

        if not os.path.exists(label_path):
            print(f"No label file found for image {image_file}")
            continue

        # Load labels
        with open(label_path, 'r') as f:
            lines = f.readlines()

        # Draw bounding boxes
        for line in lines:
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center, y_center, w, h = map(float, parts[1:])
            x_center, y_center, w, h = x_center * width, y_center * height, w * width, h * height

            x_min = int(x_center - w / 2)
            y_min = int(y_center - h / 2)
            x_max = int(x_center + w / 2)
            y_max = int(y_center + h / 2)

            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(image, str(class_id), (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        cv2.imshow('Image', image)
        cv2.waitKey(0)

    cv2.destroyAllWindows()

visualize_annotations(image_dir, label_dir, num_images=5)

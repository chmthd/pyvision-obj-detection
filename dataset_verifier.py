import os

images_dir = 'D:/Projects/Coding/deepvision/datasets/coco/images/train2017'
labels_dir = 'D:/Projects/Coding/deepvision/datasets/coco/labels/train2017'

for image_file in os.listdir(images_dir):
    image_file_name = os.path.splitext(image_file)[0]
    label_file = image_file_name + '.txt'
    label_file_path = os.path.join(labels_dir, label_file)

    if not os.path.exists(label_file_path):
        print(f"Missing label file for image: {image_file}")

for label_file in os.listdir(labels_dir):
    label_file_name = os.path.splitext(label_file)[0]
    image_file = label_file_name + '.jpg'
    image_file_path = os.path.join(images_dir, image_file)

    if not os.path.exists(image_file_path):
        print(f"Missing image file for label: {label_file}")

print("Dataset verification completed.")

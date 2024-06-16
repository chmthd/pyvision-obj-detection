import os

def create_file_list(image_dir, output_file, relative_path_prefix, label_dir):
    with open(output_file, 'w') as f:
        for image_name in os.listdir(image_dir):
            image_path = os.path.join(relative_path_prefix, image_name).replace('\\', '/')
            label_name = os.path.splitext(image_name)[0] + '.txt'
            label_path = os.path.join(label_dir, label_name).replace('\\', '/')
            print(f"Looking for label file: {label_path}")
            if os.path.exists(label_path):
                f.write(f"{image_path}\n")
            else:
                print(f"WARNING: Label file for {image_name} not found.")

# Train
train_image_dir = 'D:/Projects/Coding/deepvision/datasets/coco/train2017'
train_label_dir = 'D:/Projects/Coding/deepvision/datasets/coco/labels/train2017'
train_output_file = 'train_list.txt'
create_file_list(train_image_dir, train_output_file, 'datasets/coco/train2017', train_label_dir)

# Validation
val_image_dir = 'D:/Projects/Coding/deepvision/datasets/coco/val2017'
val_label_dir = 'D:/Projects/Coding/deepvision/datasets/coco/labels/val2017'
val_output_file = 'val_list.txt'
create_file_list(val_image_dir, val_output_file, 'datasets/coco/val2017', val_label_dir)

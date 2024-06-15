import os
import json
from tqdm import tqdm
from pycocotools.coco import COCO

def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[2] / 2.0) * dw
    y = (box[1] + box[3] / 2.0) * dh
    w = box[2] * dw
    h = box[3] * dh
    return (x, y, w, h)

def convert_annotation(data_dir, image_id, coco, output_dir):
    filename = os.path.join(data_dir, 'images', image_id + '.jpg')
    if not os.path.exists(filename):
        return

    ann_ids = coco.getAnnIds(imgIds=image_id)
    anns = coco.loadAnns(ann_ids)
    img = coco.loadImgs(image_id)[0]
    width = img['width']
    height = img['height']

    with open(os.path.join(output_dir, image_id + '.txt'), 'w') as out_file:
        for ann in anns:
            category_id = ann['category_id']
            box = convert((width, height), ann['bbox'])
            out_file.write(str(category_id) + " " + " ".join([str(a) for a in box]) + '\n')

def main():
    data_dir = 'datasets/coco'
    output_dir = 'datasets/coco/labels'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for dataset in ['train2017', 'val2017']:
        ann_file = os.path.join(data_dir, 'annotations', 'instances_{}.json'.format(dataset))
        coco = COCO(ann_file)

        image_ids = coco.getImgIds()
        for image_id in tqdm(image_ids):
            convert_annotation(data_dir, str(image_id).zfill(12), coco, os.path.join(output_dir, dataset))

if __name__ == '__main__':
    main()

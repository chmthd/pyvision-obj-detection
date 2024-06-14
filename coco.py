import os
import requests
from zipfile import ZipFile
from tqdm import tqdm

# URLs for COCO dataset
urls = {
    "train_images": "http://images.cocodataset.org/zips/train2017.zip",
    "val_images": "http://images.cocodataset.org/zips/val2017.zip",
    "annotations": "http://images.cocodataset.org/annotations/annotations_trainval2017.zip"
}

dataset_dir = "datasets/coco"

os.makedirs(dataset_dir, exist_ok=True)

def download_and_extract(url, save_path):
    local_filename = os.path.join(save_path, url.split("/")[-1])
    
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        block_size = 1024
        t = tqdm(total=total_size, unit='iB', unit_scale=True)
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=block_size):
                t.update(len(chunk))
                f.write(chunk)
        t.close()
    
    with ZipFile(local_filename, "r") as zip_ref:
        zip_ref.extractall(save_path)

    os.remove(local_filename)

for key, url in urls.items():
    download_and_extract(url, dataset_dir)

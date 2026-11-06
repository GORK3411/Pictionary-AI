import argparse
from pathlib import Path
from constants import CATEGORIES_PATH,RAW_DATA_PATH,PROCESSED_DATA_PATH
import categories.categories as c
import urllib.request, urllib.parse
import os
import json
import copy

"""
inputs:
- categories: list containing categories name

description:
download the simplified file for each category and save it in the data/raw directory
NOTE : need to add try catch in case the category doesn't exist
"""
def extract(categories : list[str]):
    base = "https://storage.googleapis.com/quickdraw_dataset/full/simplified/"
    #out_dir = os.path.join("data","raw")
    out_dir = RAW_DATA_PATH
    os.makedirs(out_dir, exist_ok=True)
    for cat in categories:
        path = os.path.join(out_dir, f"{cat}.ndjson")
        if os.path.exists(path):                      # skip files already downloaded
            print(f"skip  {cat}")
            continue
        url = base + urllib.parse.quote(cat) + ".ndjson" # spaces → %20
        print(f"downloading {cat} ...")
        urllib.request.urlretrieve(url, path)

"""
inputs:
- raw_record: one record from the .ndjson files
- max_rec: maximum output length

description:
using the original drawing, create an array where each item has the following values:
- word: the label of the record
- ratio: the percentage of completeness of the drawing
- drawing: a 2d array filled with 0(empty) and 1(filled)  
"""
def transform(raw_record,max_rec):
    
    add_to_ratio = 1/max_rec
    res = []
    #empty array
    draw = [[0] * 256 for _ in range(256)]
    total_pixel_count = 0
    #xs = stroke[0], ys = stroke[1]
    for xs, ys in raw_record["drawing"]:
        for i in range(len(xs) - 1):
            total_pixel_count += draw_line(draw, xs[i], ys[i], xs[i + 1], ys[i + 1])

    draw = [[0] * 256 for _ in range(256)]
    pixel_count = 0
    threshold = 0
    for xs, ys in raw_record["drawing"]:
        for i in range(len(xs) - 1):
            pixel_count += draw_line(draw, xs[i], ys[i], xs[i + 1], ys[i + 1])
            ratio = pixel_count/total_pixel_count
            if(ratio == 1 or ratio >= threshold):
                res.append({
                    "word":raw_record["word"],
                    "completeness":ratio,
                    "drawing":copy.deepcopy(draw),
                })
                threshold+=add_to_ratio
    return res

"""
inputs:
- draw: 2d array to edit
- x0: x of the first point
- y0: y of the first point
- x1: x of the second point
- y1: y of the second point

description:
create a fill the 2d array "draw" so that there is a line between teh first and second point
"""
def draw_line(draw, x0, y0, x1, y1):
    """Set every pixel on the line from (x0, y0) to (x1, y1)."""
    steps = max(abs(x1 - x0), abs(y1 - y0), 1)
    for t in range(steps + 1):
        x = round(x0 + (x1 - x0) * t / steps)
        y = round(y0 + (y1 - y0) * t / steps)
        draw[y][x] = 1
    return steps + 1

"""
inputs:
- records: array of records to add
- file_path: the file to append

description:
append the file with the new records
"""

def load(records,file_path):
    json_records = []
    for rec in records:
        json_records.append(json.dumps(rec)+"\n")
    with open(file_path,"a") as f:
        f.writelines(json_records)
        

"""
size is how many categories we want
image_per_category is how images from the original dataset we want for each category
max_rec is how many record we can generate from one image
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("size",type=int,default=10)
    parser.add_argument("images_per_category",type=int,default=10)
    parser.add_argument("max_rec",type=int,default=10)
    args = parser.parse_args()
    size = args.size
    images_per_category = args.images_per_category
    max_rec = args.max_rec
    print(size)
    categories_path = CATEGORIES_PATH/(str(size)+".txt")

    if(not categories_path.exists()):
        exit
    categories = c.get_categories(categories_path)
    extract(categories)
    for cat in categories:
        
        cur_in_file = os.path.join(RAW_DATA_PATH,f"{cat}.ndjson")
        cur_out_file = os.path.join(PROCESSED_DATA_PATH,f"{cat}.ndjson")
        counter = 0
        
        with open(cur_out_file,"w"):
            pass

        with open(cur_in_file,"r") as f:
            for line in f:
                raw_record = json.loads(line)
                processed_records = transform(raw_record,max_rec)
                load(processed_records,cur_out_file)
                counter+=1
                if(counter>=images_per_category):
                    break
    print("done")
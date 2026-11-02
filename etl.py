import argparse
from pathlib import Path
from constants import CATEGORIES_PATH
import categories.categories as c
import urllib.request, urllib.parse
import os
import json
"""
input: categories_names
"""
def extract(categories : list[str]):
    base = "https://storage.googleapis.com/quickdraw_dataset/full/simplified/"
    out_dir = os.path.join("data","raw")
    os.makedirs(out_dir, exist_ok=True)
    for cat in categories:
        path = os.path.join(out_dir, f"{cat}.ndjson")
        if os.path.exists(path):                      # skip files already downloaded
            print(f"skip  {cat}")
            continue
        url = base + urllib.parse.quote(cat) + ".ndjson" # spaces → %20
        print(f"downloading {cat} ...")
        urllib.request.urlretrieve(url, path)

def transform_load(categories : list[str]):
    #initialize in and out paths
    in_dir = os.path.join("data","raw")
    out_dir = os.path.join("data","processed")
    os.makedirs(out_dir, exist_ok=True)

    for cat in categories:
        # foreach element in the file, take the record and remove useless keys
        cur_in_path = os.path.join(in_dir,f"{cat}.ndjson")
        cur_out_path = os.path.join(out_dir,f"{cat}.ndjson")
        records = []
        removed_keys = ["countrycode","timestamp","recognized"]
        with open(cur_in_path,"r") as f:
            for line in f:
                r = json.loads(line)
                for key in removed_keys:
                    del r[key]
                records.append(r)
        #write the new records in a file
        with open(cur_out_path,"w") as f:
            for r in records:
                f.write(json.dumps(r)+"\n")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("size",type=int,default=10)
    args = parser.parse_args()
    size = args.size
    print(size)
    file_path = CATEGORIES_PATH/(str(size)+".txt")

    if(not file_path.exists()):
        exit
    categories = c.get_categories(file_path)
    extract(categories)
    transform_load(categories)    
    print("done")
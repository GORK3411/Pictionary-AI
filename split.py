import os 
import json
from constants import SEED
from sklearn.model_selection import train_test_split
if __name__ == "__main__":
    
    #read the file
    input_file = r"data\processed\cleaned.ndjson"
    word_id = {}
    with open(input_file,"r") as f:
        last_id = ""
        for line in f:
            record = json.loads(line)
            word = record["word"]
            key_id = str(record["key_id"])
            if last_id == key_id:
                continue
            last_id = key_id
            if(word not in word_id):
                word_id[word] = []
            word_id[word].append(key_id)

    #split the dictionary 80%/10%/10%
    train = []
    test = []
    val = []
    for word in word_id:
        ids = sorted(word_id[word])
        cur_train,rest = train_test_split(ids,test_size=0.2,random_state=SEED)
        cur_test,cur_val = train_test_split(rest,test_size=0.5,random_state=SEED)
        train.extend(cur_train)
        test.extend(cur_test)
        val.extend(cur_val)

    data = {
        "train":train,
        "test":test,
        "val":val
    }

    out_file = os.path.join("data","processed","split.json")
    with open(out_file,"w") as f:
        json.dump(data,f,indent=4)
    pass
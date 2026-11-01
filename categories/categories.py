from constants import SEED,CATEGORIES_PATH
import random

"""
get all categories from a file.
each category should be on a line.
"""
def get_categories(file_path):
    res = []
    with open(file_path) as f:
        for category in f:
            res.append(category.strip())
    return res


"""
save the list of categories in a file.
"""
def save_categories(categories,file_name = ""):
    if file_name == "":
        file_name = CATEGORIES_PATH/(str(len(categories))+".txt")
    with open(file_name,"w") as f:
        for c in categories:
            f.write(c)
            f.write("\n")

"""
create a new list of categories.

inputs:
must_add: all the categories that needs to be included.
all: the list of all possible categories.
num : the size of the final list
"""
def create_categories(must_add,all,num):
    res = list(must_add)
    set_res = set(res)
    random.seed(SEED)
    while len(res) < num:
        while True:
            cur = all[random.randint(0,len(all) - 1)]
            if(cur not in set_res):
                res.append(cur)
                set_res.add(cur)
                break
    return res

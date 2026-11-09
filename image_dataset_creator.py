from constants import CLEANED_PATH,SPLIT_PATH,PROCESSED_DATA_PATH
import os
import json
import torch
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
    - image: 2d array (torch tensor, numpy array or list) to display
    - title: optional text shown above the image (e.g. the label)

    description:
    open a window showing the image so the result of the drawing can be checked visually
"""
def show_image(image, title=None):
    import matplotlib.pyplot as plt
    if isinstance(image, torch.Tensor):
        image = image.cpu().numpy()
    plt.imshow(image, cmap="gray_r", interpolation="nearest")
    if title is not None:
        plt.title(title)
    plt.axis("off")
    plt.show()

"""
    inputs:
    - drawing: list of strokes, each stroke being [[x0, x1, ...], [y0, y1, ...]] with values in 0..255
    - size: width and height of the output image

    description:
    create a size x size image (0 = empty, 1 = filled) by drawing every stroke of the drawing
"""
def drawing_to_image(drawing, size=28):
    image = torch.zeros(size, size)
    scale = (size - 1) / 255
    for stroke in drawing:
        xs = stroke[0]
        ys = stroke[1]
        if len(xs) == 1:  # a stroke with a single point is just a dot
            image[round(ys[0] * scale)][round(xs[0] * scale)] = 1
        for i in range(len(xs) - 1):
            x0, y0 = round(xs[i] * scale), round(ys[i] * scale)
            x1, y1 = round(xs[i + 1] * scale), round(ys[i + 1] * scale)
            draw_line(image, x0, y0, x1, y1)
    return image

def main():
    if not os.path.exists(CLEANED_PATH) or not os.path.exists(SPLIT_PATH):
        exit() 

    with open(SPLIT_PATH,"r") as f:
        splits = json.load(f)

    res = {}
    classes = set()
    for s in splits:
        splits[s] = set(splits[s])
        res[s] = []

    print("drawing images from", CLEANED_PATH)
    drawn = 0
    with open(CLEANED_PATH,"r") as f:
        for line in f:
            record = json.loads(line)
            classes.add(record["word"])
            for s in splits:
                if record["key_id"] in splits[s]:
                    image = drawing_to_image(record["drawing"])
                    res[s].append((image, record["word"], record["completeness"]))
                    drawn += 1
                    if drawn % 1000 == 0:
                        print(drawn, "images drawn")

    print("done:", drawn, "images drawn in total")
    for s in res:
        print(" ", s, ":", len(res[s]), "images")

    classes = sorted(classes)
    word_to_idx = {w: i for i, w in enumerate(classes)}

    for s in res:
        cur_path = os.path.join(PROCESSED_DATA_PATH,s+".pt")
        images = []
        labels = []
        completeness = []
        for img,label,comp in res[s]:
            images.append(img)
            labels.append(word_to_idx[label])
            completeness.append(comp)
        torch.save({

            "images":torch.stack(images),
            "labels":torch.tensor(labels),
            "completeness":torch.tensor(completeness, dtype=torch.float32),
            "classes":classes,
            },cur_path)
        print("saved", len(images), s, "images to", cur_path)
            
        

    

main()

        
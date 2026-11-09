import torch
from torch.utils.data import Dataset

class QuickDrawDataSet(Dataset):
    def __init__(self, path, min_completeness=0.0):
        data = torch.load(path)
        keep = data["completeness"] >= min_completeness   # optional: drop near-empty drawings
        self.images = data["images"][keep]
        self.labels = data["labels"][keep]
        self.classes = data["classes"]

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        image = self.images[index].unsqueeze(0)   # (28, 28) -> (1, 28, 28) for a CNN
        return image, self.labels[index]

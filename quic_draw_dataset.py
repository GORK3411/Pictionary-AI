from torch.utils.data import Dataset

class QuickDrawDataSet(Dataset):

    def __getitem__(self, index):
        return super().__getitem__(index)

    def __len__(self):
        pass
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
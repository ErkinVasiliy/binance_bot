import os
from PIL import Image

path = r'C:\binance\to_merge'

image_pos = [(0,0), (0, 1), (1, 0), (1, 1)]
w, h = 640, 480

result = Image.new('RGB', (w * 2, h * 2))

for file, pos in zip(os.listdir(path), image_pos):
    file_path = os.path.join(path, file)
    im = Image.open(file_path)
    result.paste(im, (w * pos[0], h * pos[1]))

result.save(os.path.join(path, 'result.png'))
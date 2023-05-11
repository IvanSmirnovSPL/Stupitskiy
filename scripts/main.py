from pathlib import Path
import shutil
import os
from support import InitParams
from calculation import calculate
from PIL import Image

res_path = Path.cwd().parent / 'results'
shutil.rmtree(str(res_path), ignore_errors=True)
os.mkdir(str(res_path))

scenarios = [
    InitParams(path=res_path, a=0.5, U=0.),
    InitParams(path=res_path, a=0.9, U=0.),
    InitParams(path=res_path, a=0.5, U=2.2),
    InitParams(path=res_path, a=0.9, U=2.2),
    InitParams(path=res_path, a=0.5, U=3.0),
    InitParams(path=res_path, a=0.9, U=3.0),
    InitParams(path=res_path, a=0.5, U=3.2),
    InitParams(path=res_path, a=0.9, U=3.2),
]

for scenario in scenarios:
    calculate(scenario)


paths = [str(res_path / f) for f in os.listdir(res_path)]


def convert_images_to_pdf(images_folder, pdf_file):
    images = []
    for file in os.listdir(images_folder):
        if file.endswith(".jpg") or file.endswith(".png"):
            image = Image.open(os.path.join(images_folder, file))
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            images.append(image)
    images[0].save(pdf_file, save_all=True, append_images=images[1:])


convert_images_to_pdf(str(res_path), str(res_path / 'results_Smirnov.pdf'))

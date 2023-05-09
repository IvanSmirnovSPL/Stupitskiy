from pathlib import Path
import shutil
import os
from support import InitParams
from calculation import calculate

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

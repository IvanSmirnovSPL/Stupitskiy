from pathlib import Path
import shutil
import os
from support import InitParams
from calculation import calculate

res_path = Path.cwd().parent / 'results'
shutil.rmtree(str(res_path), ignore_errors=True)
os.mkdir(str(res_path))

scenarios = [
    InitParams(path=res_path / 'first', a=0.5, U=0.)
]

for scenario in scenarios:
    calculate(scenario)

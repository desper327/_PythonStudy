import yaml
import sys,os
import importlib

path=os.getenv("forza","")
print(path)
sys.path.append(path)

# 动态导入模块，避免pyright检查报错  import forza_utils
forza_utils=importlib.import_module("forza_utils")
Yprint=forza_utils.Yprint

file_path=r"test_yaml.yml"
with open(file_path, 'r', encoding='utf-8') as file:
    data = yaml.safe_load(file)
    Yprint(data[True])
from pathlib import Path

# 创建一个Path对象
path=Path(r"D:\ZYfile\BaiduSyncdisk\MyStudy\_python学习")

print(dir(path))
# print(path.stat())
# print(path.exists())
# print(path.is_dir())
# print(path.is_file())
# #print(path.is_mount())
# print(path.is_symlink())
# print(path.is_absolute())
# print(path.is_reserved())
# print(path.is_socket())
# print(path.is_fifo())
# print(path.is_block_device())
# print(path.is_char_device())
# #print(path.owner())
# #print(path.group())
# print(path.stem,111111)
# print(path.suffix)
# print(path.anchor)
# print(path.parents)
# print(path.parent)
# print(path.name)
# print(path.suffixes)
# print(path.parts)
# print(path.drive)
# print(path.root)

# for p in path.iterdir():
#     print(p)

for p in path.glob("*bc"):
    print("Unacceptable pattern: {!r}".format(p))



aa=path.name
print("Unacceptable pattern: {!r}".format(aa))
print("Unacceptable pattern: {!s}".format(aa))
print("Unacceptable pattern: {!a}".format(aa))

print(path.__repr__())
print(path.__str__())

import sys
sys.path.append(r"A:\temp\MayaToUE\ExHis\TBZZXKX\TD")
import batch_genUeProject_PyFile__XKX_EP01_sc100_shot0020_ANI_V007_2025_11_04_15_18_42
from pathlib import Path
import re

a=Path(r"C:\Users\wb.zhangyang21\Desktop\动画资源\动画原始资源\本体动画\0006_skateboard_9.max")

print(a.stem)

pattern=r"_[0-7]$"

b=re.search(pattern, a.stem)

if b:
    print("Match",b.group(0).replace("_", ""))
else:
    print("No match")


b=Path("")
if b:
    print(bool(b))

path=Path(r"D:\P4WorkSpace\Z\inner01\guangzhou\G18项目美术资源\P4V目录\4)美术最终输出资源与程序工具\2)美术最终输出资源\1）角色PNG输出提交")
folder = [str(folder) for folder in path.rglob('*') if folder.is_dir() and folder.name.lower().startswith('4422')]
print(folder)

print(str(None))


p4_produce_path=r"D:/P4WorkSpace/Z/inner01/guangzhou/G18项目美术资源/P4V目录/2)美术资源制作目录/2)制作资源/角色/6坐骑/"
path = Path(p4_produce_path.split("6坐骑")[0]) / "6坐骑" / "4616"
print(path.exists())
print(f"{path}")


if [None]:
    print("yes")

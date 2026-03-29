import re,os


for current_file_name in os.listdir(r"D:\P4WorkSpace\Z\inner01\guangzhou\G18项目美术资源\P4V目录\2)美术资源制作目录\2)制作资源\角色\6坐骑\4575纸盒猫猫\max"):
    current_file_name= os.path.splitext(current_file_name)[0]
    pattern=r"_(stand|walk)[_]?"
    match=re.search(pattern, current_file_name)
    # if match:
    #     print(current_file_name, "okokokok")
    # else:
    #     print(current_file_name, "no no")

    # pattern15=r"_seesawwalk[2-3]"
    # match15=re.search(pattern15, current_file_name)
    # if match15:
    #     print(current_file_name, "okokokok15")
    # else:
    #     print(current_file_name, "no no 15")


    pattern=r"_[0-7][_]?"
    match=re.search(pattern, current_file_name)
    if match:
        print(current_file_name, "okokokok")
    else:
        print(current_file_name, "no no")


import csv
from pathlib import Path


def find_all_file(src_dir) -> list:
    ignores = [".DS_Store", "Thumbs.db"]
    result = []
    for i in Path(src_dir).iterdir():
        if not i.name in ignores:
            if i.is_file():
                result.append(i)
            else:
                for x in find_all_file(i):
                    result.append(x)
    return result


def check_csv(existing_file, csv_file):
    exclude_list = []
    for i in existing_file:
        if not i in csv_file:
            exclude_list.append(i)

    return exclude_list


def get_theory_path(res_file, file_chapter, file_topic, file_name):
    # 检查文件是否存在，返回图片路径
    image_path = Path(res_file, file_chapter, file_topic, file_name)
    if not image_path.exists():
        print(f"{image_path} not exists")
    return image_path


def find_file_using_name(file_name, file_library):
    for item in file_library:
        if file_name == item.name:
            return item
    return Path("res/pictures", file_name)


with open("res/picture.csv", newline="") as f:
    reader = csv.DictReader(f)
    theoty_path_list = []
    print("========================! ( ⊙ o ⊙ ) !===========================")
    for row in reader:
        # 检查csv中的图片是否都存在
        theoty_path_list.append(
            get_theory_path(
                "res/pictures", row["Chapter"], row["Topic"], row["File Name"]
            )
        )
    print("========================! ( ⊙ o ⊙ ) !===========================")

    auto_path_result = []
    for i in check_csv(find_all_file("res/pictures"), theoty_path_list):
        print(f"{i} is not in place")

        auto_path = find_file_using_name(i.name, theoty_path_list)
        i.rename(auto_path)
        auto_path_result.append(f"moved {i} to {auto_path}")

    if not auto_path_result == []:
        for x in auto_path_result:
            print(x)

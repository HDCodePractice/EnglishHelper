import csv
from os import remove, rename
from pathlib import Path


# get all the file under the folder or folder in folder
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


# compare the existing file Path list to theory file Path list
def check_csv(existing_file, csv_file):
    exclude_list = []
    for i in existing_file:
        if not i in csv_file:
            exclude_list.append(i)

    return exclude_list


# get theory path from csv document
def get_theory_path(res_file, file_chapter, file_topic, file_name):
    image_path = Path(res_file, file_chapter, file_topic, file_name)
    if not image_path.exists():
        print(f"{image_path} not exists")
    return image_path


# find file's theory path according to file name, if file name not exist in document, return source folder
def find_file_using_name(file_name, file_library):
    for item in file_library:
        if file_name == item.name:
            return item
    return Path("res/pictures", file_name)

# enter src folder path, get theory path from name
# remove the old one and replace with the new one in source folder


def replace_new_file(src_dir):
    ignores = ['.DS_Store', 'Thumbs.db']
    src_file = []
    theoty_path_list = []
    with open('res/picture.csv', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            theoty_path_list.append(get_theory_path(
                'res/pictures', row["Chapter"], row["Topic"], row["File Name"]))
    for i in Path(src_dir).iterdir():
        if not i.name in ignores:
            if i.is_file():
                src_file.append(i)
    for src_file in src_file:
        file_theory = find_file_using_name(src_file.name, theoty_path_list)
        if file_theory.exists():
            remove(file_theory)
            rename(src_file, file_theory)


def main_execute():
    with open('res/picture.csv', newline='') as f:
        reader = csv.DictReader(f)
        theoty_path_list = []
        for row in reader:
            theoty_path_list.append(get_theory_path(
                'res/pictures', row["Chapter"], row["Topic"], row["File Name"]))
        print("========================! ( ⊙ o ⊙ ) !===========================")

        auto_path_result = []
        for i in check_csv(find_all_file('res/pictures'), theoty_path_list):
            print(f"{i} is not in place")

            auto_path = find_file_using_name(i.name, theoty_path_list)
            i.rename(auto_path)
            auto_path_result.append(f"moved {i} to {auto_path}")

        if not auto_path_result == []:
            for x in auto_path_result:
                print(x)


replace_new_file("res/pictures")

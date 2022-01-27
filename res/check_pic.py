import csv
from pathlib import Path

# res/pictures/Health/Symptoms and Injuries
# res/pictures/chapter/topic/words/filename


# def move_log(res_path, dest_path):
#     return ''


def find_all_file(src_dir) -> list:
    ignores = ['.DS_Store', 'Thumbs.db']
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
    image_path = Path(res_file, file_chapter, file_topic, file_name)
    if not image_path.exists():
        print(f"{image_path} not exists")
    return image_path


# def move_file(res_file, file_chapter, file_topic, file_name):
#     return ''
with open('res/picture.csv', newline='') as f:
    reader = csv.DictReader(f)
    theoty_path_list = []
    for row in reader:
        theoty_path_list.append(get_theory_path(
            'res/pictures', row["Chapter"], row["Topic"], row["File Name"]))

    for i in check_csv(find_all_file('res/pictures'), theoty_path_list):
        print(f"{i.name} is not in place")


# search_all_file(find_all_file("res/pictures"), "courthouse.jpg")

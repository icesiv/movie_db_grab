import random
import ntpath

import string
import re
from abc import ABC

from html.parser import HTMLParser

##
# Strip HTML Tags
# --------------------------
# strip_tags(html)


class MLStripper(HTMLParser, ABC):
    def __init__(self):
        super().__init__()
        self.reset() 
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data().strip()


def remove_multi(main_text, text_to_remove):
    for s in text_to_remove:
        main_text = main_text.replace(s, '')

    return main_text


def clean_result(result, text_to_remove=None, default='-', single_line=False):
    if result is None:
        return default

    result = strip_tags(result)

    if text_to_remove is not None:
        remove_multi(result, text_to_remove)

    result = result.strip()

    if single_line:
        result = result.replace('\n', ' ').replace('\r', ' ')

    result = re.sub(' +', ' ', result)

    if result is '':
        return default

    return result


def safe_split(txt, separator, index_needed):
    t = txt.split(separator)

    if index_needed == 0:
        return t[0]
    elif index_needed > len(t) + 1:
        return '-'
    else:
        return t[index_needed]

##
# Random Generator
# --------------------------
# id_generator()
# >>> 'G5G74W'
#
# id_generator(3, "6793YUIO")
# >>>'Y3U'
##


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# #
# Extract Images From Text
# Changes Name in main


def extract_link_from_text(text_with_image, web_safe_topic, new_name):
    image_string = ""
    images = re.findall(r"\/images\/.*?JPG", text_with_image, re.MULTILINE)
    images += re.findall(r"\/images\/.*?jpg", text_with_image, re.MULTILINE)
    images += re.findall(r"\/images\/.*?PNG", text_with_image, re.MULTILINE)
    images += re.findall(r"\/images\/.*?png", text_with_image, re.MULTILINE)

    img_count = 0

    web_safe_topic = web_safe_topic + "/"

    for j in images:
        img_count += 1

        new_dir_name = ntpath.dirname(j) + "/"
        new_dir_name = new_dir_name.replace("solution-image/", "")
        new_dir_name = new_dir_name.replace(web_safe_topic, "")
        # new_dir_name = new_dir_name.replace(
        #     config.IMAGE_LINK_OLD, config.IMAGE_LINK_NEW)

        new_file_name = "{0}-{1}.png".format(
            web_safe_topic + new_name, img_count)
        new_file_path = new_dir_name + new_file_name

        text_with_image = text_with_image.replace(j, new_file_path)
        image_string = image_string + j + ":" + new_file_path + "|"

    return text_with_image, image_string


def count_lines(file_path):
    with open(file_path) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def look_for_child(data, key_arr):
    size = len(key_arr)

    if isinstance(data, list):
        i = int(key_arr[0])
        if i < len(data):
            result = data[i]
            if size > 1:
                del key_arr[0]
                return look_for_child(result, key_arr)
            else:
                return result
        else:
            return "-"
    else:
        if data.get(key_arr[0]):
            result = data.get(key_arr[0])
            if size > 1:
                del key_arr[0]
                return look_for_child(result, key_arr)
            else:
                return result


def item_finder(data, idx_string):
    key_arr = [i for i in idx_string[1:-1].split('][')]
    return look_for_child(data, key_arr)

def str_join(arr_string, separetor = ""):
    data = ""
    for s in arr_string:
        if(s):
            data += str(s) + separetor
        
    return data

# # find all idem with same id
# d = { "id" : "abcde",
#     "key1" : "blah",
#     "key2" : "blah blah",
#     "nestedlist" : [
#     { "id" : "qwerty",
#         "nestednestedlist" : [
#         { "id" : "xyz", "keyA" : "blah blah blah" },
#         { "id" : "fghi", "keyZ" : "blah blah blah" }],
#         "anothernestednestedlist" : [
#         { "id" : "asdf", "keyQ" : "blah blah" },
#         { "id" : "yuiop", "keyW" : "blah" }] } ] }


# def fun(d):
#     if 'id' in d:
#         yield d['id']
#     for k in d:
#         if isinstance(d[k], list):
#             for i in d[k]:
#                 for j in fun(i):
#                     yield j

# print(list(fun(d)))

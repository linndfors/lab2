from hmac import digest
import json

def parse_kved():
    '''
    Thist function open json file, read it and save data
    '''
    with open('twiter1.json') as my_file:
        data = json.load(my_file)
        return data[0]

def key_search(data):
    '''
    Return keys from json file
    '''
    choice = {}
    data_keys = [elem for elem in data.keys()]
    for section in data_keys:
        content = dig_into(data, choice, section)
        choice.update(content)
    return choice

def dig_into(section, choice_dict, elem):
    if type(section) == list:
        section= section[0]
    content = section.get(elem)
    choice_dict[elem] = content
    content_type = type(content)
    if content_type == dict:
        inside_keys = content.keys()
        for numb in inside_keys:
            dig_into(content, choice_dict, numb)
        return choice_dict
    if content_type == list:
        if '{' in content:
            inside_keys = [thing for thing in content]
            if type(inside_keys) == list and inside_keys:
                inside_keys = inside_keys[0]
            for numb in inside_keys:
                dig_into(content, choice_dict, numb)
        else:
            choice_dict[elem] = content
        return choice_dict
    else:
        return choice_dict

def find_key(data, request):
    for key_elem in data:
        if key_elem == request:
            answer = data[key_elem]
            if type(answer) == dict or type(answer) == list:
                a_ans = input("By the way it include other objects\n\
Maybe you prefer to chose only one from this? y/n\n")
                if a_ans == 'y':
                    if type(answer) == dict:
                        print([elem for elem in answer.keys()])
                    if type(answer) == list:
                        new_dict = answer[0]
                        print([elem for elem in new_dict.keys()])
                    new_request = input('So put a new request:\n')
                    # new_list = [elem for elem in answer.keys()]
                    answer = find_key(data, new_request)
            return answer


data = parse_kved()
keys_info = key_search(data)
print('You have such choices:\n', [elem for elem in keys_info.keys()])
# request = 'user'
request = input('Which you want to know about?\n')
print(find_key(keys_info, request))

        
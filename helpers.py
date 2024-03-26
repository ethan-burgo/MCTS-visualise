def remove_last_comma(input_string):
        last_comma_index = input_string.rfind(',')
        if last_comma_index != -1:
            return input_string[:last_comma_index] + input_string[last_comma_index+1:]
        else:
            return input_string


def format_update_statement(values_dict):
    update_string = ""
    for k, v in values_dict.items():
        update_string = update_string + str(k) + " = " + "'"+str(v)+"'" + ","
    update_string = remove_last_comma(update_string)
    return update_string

def format_id(id):
    return "'" + str(id) + "'"

def remove_str_list(input_list):
    list_string = ""
    for val in str(input_list):
         if val != "'" and val != '"':
              list_string += val
    if list_string == "":
         return "[]"
    return list_string


import os
from os.path import join, getsize
import stat


class System_Object(object):

    def __init__(self, dir_path):
        self.path = dir_path
        
        if os.path.isfile(dir_path):
            self.is_file = True
        if os.path.isdir(dir_path):
            self.is_file = False
        self.set_name_num_format(dir_path)

    def __repr__(self):
        return self.__str__() + '!'

    def __str__(self):
        return str(self.number)

    def set_name_num_format(self, full_path):
        if self.is_file:
            self.set_name_num_format_file(full_path)
        else:
            self.set_name_num_format_dir(full_path)

    def set_name_num_format_file(self, full_path):
        if '.' in full_path:
            name_form = full_path.rsplit('.', maxsplit=1)
            self.form = name_form[-1]
            name = name_form[0]
        else:
            self.form = ''
            name = full_path 
        self.set_params(name)    

    def set_name_num_format_dir(self, full_path):
        self.form = ''
        self.set_params(full_path)

    def set_params(self, full_path):
        path_nam = full_path.rsplit('\\', maxsplit=1)
        full_name = path_nam[-1]
        self.root = path_nam[0]
        self.set_name_number(full_name)

    def set_name_number(self, full_name):
        name_number = full_name.rsplit('_' , maxsplit=1)
        try: 
            _ = int(name_number[-1])
            is_int = True
        except:
            is_int = False
        if is_int and len(name_number[-1]) == 3:
            name = name_number[0]
            number_txt = name_number[-1]
        else:
            name = full_name
            number_txt = ''
        self.name = name
        self.number_txt = number_txt
        self.set_number(number_txt)

    def set_number(self, number_txt):
        if not len(number_txt) < 1:
            number = number_txt
        else:
            number = "-1"
        self.number = int(number)  

    def get_spec_name(self):
        if self.is_file and not self.form == '':
            dot = '.'
        else:
            dot = ''
        return self.name + dot + self.form

    def get_spec_path(self):
        if self.is_file and not self.form == '' :
            dot = '.'
        else:
            dot = ''
        return self.root + '\\' + self.name + dot + self.form

    def delete(self):
        if self.is_file:
            os.chmod(self.path , stat.S_IWRITE)
            os.remove(self.path)    
        else:
            os.chmod(self.path , stat.S_IWRITE)
            os.rmdir(self.path)

    def rename(self, new_path=None):
        if new_path:
            new_path = self.get_spec_path()
        os.chmod(self.path , stat.S_IWRITE)
        os.rename(self.path, new_path)   

def delete_and_rename_EaseUS_in_all_directories(dir_path):
    delete_EaseUS_in_directory(dir_path)
    rename_EaseUS(dir_path)
    with os.scandir(dir_path) as it:
        for root in it:
            if os.path.isdir(root.path):
                delete_and_rename_EaseUS_in_all_directories(root.path)

def delete_EaseUS_in_directory(dir_path):
    print(dir_path)
    dic_dir = get_system_objects_to_dic(dir_path)
    print(dic_dir)

    for name, numbers in dic_dir.items():
        numbers_list = [o.number for o in numbers] 
        if numbers_list == ['-1']:
            continue
        max = get_max(numbers_list)
        
        list_objects_to_delete = get_list_objects_to_delete(numbers, max)
        #print(name, numbers_list, max, list_objects_to_delete)
        #print( name, numbers_list, max, [o.path for o in list_objects_to_delete])
        for object_to_delete in list_objects_to_delete: object_to_delete.delete()
                    
def get_system_objects_to_dic(path):
    dic_dir = dict()
    with os.scandir(path) as it:
        for root in it:
            print(root.path)
            so = System_Object(root.path)

            if so.get_spec_name() not in dic_dir:
                dic_dir[so.get_spec_name()] = []
            dic_dir[so.get_spec_name()].append(so)          
    return dic_dir

def get_max(numbers):
    max = -2
    for num in numbers:
            n = int(num)
            if n > max:
                max = n
    return max

def get_list_objects_to_delete(objects, max):
    list_objects_to_delete = []
    for os in objects:
            n = os.number
            if n != max:
                list_objects_to_delete.append(os)
    return list_objects_to_delete
    
def rename_EaseUS(path):
    with os.scandir(path) as it:
        for root in it:
            so = System_Object(root.path)
            print(so.path, ' => ', so.get_spec_path())
            new_path = so.get_spec_path()
            if not new_path == so.path:
                so.rename(new_path)
           
dir_path = "C:\\path\\to\\dir"

delete_and_rename_EaseUS_in_all_directories(dir_path)

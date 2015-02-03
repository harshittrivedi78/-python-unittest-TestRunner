from collections import namedtuple
import json


__author__ = 'Harshit'
__version__ = '5.3.0'



'''
JSON Serialization and De-serialization : Lambda Functions
'''

serialize = lambda cls_obj : json.dumps(cls_obj , default=lambda o: o.__dict__, sort_keys=True, indent=4)

deserialize = lambda json_string : json.loads(json_string, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))


def SaveAs(filepath , filename , output):
    """
    @description: Save the file into filepath location with the filename as of filename arg and output is the string which you want to write
                  into this file.
                  
    @param filepath: Positional argument must be provided. This is the location where you are going to save your file.
    @param filename: Positional argument must be provided. This is the name of your file with which it will be saved. 
    @param output: Positional argument must be provided. This is the Output string which you want to write into your file.
    """
    with open(filepath + '\\' + filename , 'w') as f:
        f.write(str(output))
        f.close()
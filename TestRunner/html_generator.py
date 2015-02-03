__author__ = 'Harshit'
__version__ = '5.3.0'

import os
import time

def Generate(converter , xml_filepath , save_html_file_here , html_file_name , keep_xml = False):
    try:
        if converter is not None:
            batch_string = ''' @echo off \n
            "{0}" "{1}" "{2}" \n '''.format(converter , xml_filepath  , save_html_file_here + '\\' + html_file_name)
            with open(save_html_file_here + "\\converter.bat", 'w') as f:
                f.write(batch_string)
                f.close()
            from subprocess import Popen
            p = Popen(save_html_file_here + "\\converter.bat")
            time.sleep(3)
            p.kill()
        else:
            pass
        if keep_xml is False:
            os.remove(xml_filepath)
        else:
            pass
        os.remove(save_html_file_here + "\\converter.bat")
    except :
        raise ValueError("Converter file not defined.")


import os


def input_check(msg, not_null, path_type=''):
    the_input = input(msg)
    while True:
        if not_null and not the_input:
            the_input = input(f'输入不可为空, {msg}')
        elif path_type == 'file' and not os.path.isdir(the_input):
            the_input = input(f'输入不是文件, {msg}')
        elif path_type == 'dir' and not os.path.isdir(the_input):
            the_input = input(f'输入不是文件夹, {msg}')
        else:
            return the_input

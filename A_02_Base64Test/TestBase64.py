import base64
import os

dir_path = input('请输入要遍历的目录:')

def file_to_base64(file_name):
    file_path = os.path.join(dir_path, file_name)
    file_size = os.path.getsize(file_path)
    with open(file_path, 'rb') as file:
        # 读取文件内容
        data = file.read()
        # 使用base64.b64encode对数据进行编码
        encoded_data = base64.b64encode(data)
        # 将编码后的数据转换为字符串
        base64_str = encoded_data.decode('utf-8')
        base64_length = len(base64_str)
        byte_array = base64_str.encode()
        re_byte_size = len(byte_array)
        print(f"文件{file_name}的大小为{file_size}bytes, 转换为base64字符串的长度为{base64_length}, 比率{base64_length/file_size}, 再次转为二进制的大小为{re_byte_size}")


# 测试函数
# file_path = 'your_file_path.txt' # 将此处替换为你的文件路径

file_list = os.listdir(dir_path)
for file in file_list:
    if os.path.isfile(os.path.join(dir_path, file)):
        print(f"{file}是一个文件")
        file_to_base64(file)
# print(base64_str)

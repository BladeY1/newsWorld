# 定义文件路径
file_path = './2_log1'

# 读取文件并删除指定行后的内容
def truncate_file(file_path, line_number):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 保留指定行之前的内容
    lines = lines[:line_number]

    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

# 执行函数，删除第3565行之后的内容
truncate_file(file_path, 20000)

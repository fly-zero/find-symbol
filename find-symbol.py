# 查找 Linux 动态库和静态中的符号
# Usage: python find-symbol.py <symbol> <lib-path> ...

import sys
import os
import subprocess

def find_symbol(symbol, lib_path):

    # 判断是否为文件
    if not os.path.isfile(lib_path):
        return False

    nm_flag = None

    # 判断是否为动态库
    if lib_path.endswith('.so'):
        nm_flag = '-CD'
    elif lib_path.endswith('.a'):
        nm_flag = '-C'
    else:
        return False

    # 执行命令，输出到字符串，并捕获异常，忽略 stderr
    try:
        output = subprocess.check_output(['nm', nm_flag, lib_path], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return False

    # 分解字符串
    target_symbol_bytes = symbol.encode('utf-8')
    lines = output.splitlines()

    # 逐行匹配
    for line in lines:
        if (len(line) < 19): # 判断是否为合法的行
            continue

        symbol_type = line[17] # 获取符号类型
        if not symbol_type in b'TtWw': # 判断是否为 T、t、W、w 类型的符号
            continue

        symbol_name = line[19:] # 获取符号名称
        if symbol_name == target_symbol_bytes: # 判断是否为目标符号
            return True

    return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python find-symbol.py <symbol> <lib-path> ...')
        sys.exit(1)

    symbol = sys.argv[1]
    lib_path_list = sys.argv[2:]

    for lib_path in lib_path_list:
        if find_symbol(symbol, lib_path):
            print(lib_path)
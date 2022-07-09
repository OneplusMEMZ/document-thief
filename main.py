import psutil
import threading
import shutil
import zipfile   # 导入zipfile,这个是用来做压缩和解压的Python模块；
import os
import time


driver = ""
flag = 0


def mkdir(path):
    """
    创建指定的文件夹
    :param path: 文件夹路径，字符串格式
    :return: True(新建成功) or False(文件夹已存在，新建失败)
    """
    # 引入模块

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
         # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False

def del_file(path_data):
    for i in os.listdir(path_data) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "\\" + i#当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == True:#os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            os.remove(file_data)
        else:
            del_file(file_data)




def batch_zip(start_dir,zip_file) -> object:
    # start_dir要压缩的文件路径
    # zip_file 输出zip文件的路径
    zip_file = zip_file + '.zip'
    z = zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED)
    print(z)
    for path, dirname, file_name in os.walk(start_dir):
#         print("文件夹根路径：", path)
        fpath = path.replace(start_dir, '') # 去除根路径名称
#         print("--去除根路径：", fpath)
        fpath = fpath and fpath + os.sep   # 在原fpath加上\
#         print("****去除根路径+\ ：", fpath)

        for filename in file_name: # 逐个循环读取文档名称
#             print('--', fpath+filename)
#             fpath + filename完整构成每个文档的去根绝对路径
#             s = os.path.join(path, filename)   # 补齐全部的绝对路径
#             print('*-*',s)

            z.write(os.path.join(path, filename), fpath + filename) # 实现在输出路径的Zip压缩操作
    z.close()
    return zip_file


def find_epub(file_path, target, result):  # 寻找epub文件
    files = os.listdir(file_path)  # 找到路径中的所有文件
    for f in files:
        npath = file_path + '/' + f  # 路径+文件名
        if os.path.isfile(npath):
            if os.path.splitext(npath)[1] == target:  # 匹配目标 .epub
                result.append(npath)
        if os.path.isdir(npath):
            if f[0] == '.':
                pass
            else:
                find_epub(npath, target, result)
    return result


def copy_file(result):  # 复制epub文件
    file_path2 = r"C:\doc_without_zip"  # 复制到路径
    for file in result:
        print(str(file).split("/")[-1])  # 书名
        file2 = file_path2 + "/" + str(file).split("/")[-1]  # 路径+书名
        shutil.copy(file, file2)  # 复制文件





def watch_upan():
    global driver, flag
    while True:
        if driver != "":
            file_path = driver
            result = []
            find_epub(file_path, ".doc", result)
            copy_file(result)
            find_epub(file_path, ".docx", result)
            copy_file(result)
        time.sleep(300)
        for item in psutil.disk_partitions():
            if "removable" in item.opts:
                driver,opts = item.device,item.opts
                print(driver)
                flag = 2
                break
            else:
                continue
        if flag == 2:
            break
def zip_file():
    while True:
        time.sleep(300)
        batch_zip("C:\doc_without_zip","C:\114514")
        del_file(r"C:\doc_without_zip")

mkdir(r"C:\doc_without_zip")
mkdir(r"C:\114514")
start_watch_upan=threading.Thread(target=watch_upan)
start_zip_file=threading.Thread(target=zip_file)
start_watch_upan.start()
start_zip_file.start()

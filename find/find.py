#_*_coding:utf-8_*_
import re
import sys
import pathlib
import time

class Find:
    def __init__(self,path,command):
        self.path = path
        self.command = command
        self.file_list = []

    def name(self,name_pattern):
        name_list = []
        f = pathlib.Path(self.path)
        if f.is_dir():
            for patt in name_pattern:
                for i in f.rglob(patt):
                    name_list.append(i)
        return name_list

    def iname(self,name_pattern):
        iname_list = []
        f = pathlib.Path(self.path)
        if f.is_dir():
            for patt in name_pattern:
                for i in f.rglob(patt):
                    iname_list.append(i)
        return iname_list

    def size(self,size_pattern):
        size_file = []
        name_pattern = "*"
        file = pathlib.Path(self.path)
        total = 0
        flag = size_pattern[0][0]
        if flag == "+":
            if str(size_pattern[0][1:]).isdigit():
                size_pattern = int(size_pattern[0][1:])
                if file.is_dir():
                    for f in file.rglob(name_pattern):
                        if f.stat().st_size/1024 > size_pattern:
                            size_file.append(f)
            return size_file

        elif flag == "-":
            if str(size_pattern[0][1:]).isdigit():
                size_pattern = int(size_pattern[0][1:])
                if file.is_dir():
                    for f in file.rglob(name_pattern):
                        if f.stat().st_size/1024 < size_pattern:
                            size_file.append(f)
            return size_file

        elif str(size_pattern[0]).isdigit():
            if file.is_dir():
                for f in file.rglob(name_pattern):
                    if f.stat().st_size/1024 > int(size_pattern[0]) - 1:
                        if f.stat().st_size/1024 > int(size_pattern[0]):
                            continue
                        size_file.append(f)
            return size_file

    def atime(self,atime_pattern):
        atime_list = []
        file = pathlib.Path(self.path)
        name_pattern = "*"
        now_time = time.time()
        total = 0
        if atime_pattern[0].isdigit():
            atime_pattern = int(atime_pattern[0])
            atime_pattern = atime_pattern * 86400

            if file.is_dir():
                for f in file.rglob(name_pattern):
                    try:    #find /path -atime number_#，我理解的是查找大于等于number_#天数、且小于number_# + 1的文件
                        if time.time() - f.stat().st_atime > atime_pattern:
                            if time.time() - f.stat().st_atime <= atime_pattern + 86400:
                                atime_list.append(f)
                    except FileNotFoundError:   #有些链接文件会产生错误
                        pass
                return atime_list

        elif atime_pattern[0][0] == "+":
            atime_pattern = int(atime_pattern[0][1:])
            atime_pattern = atime_pattern * 86400

            if file.is_dir():
                for f in file.rglob(name_pattern):
                    try: #find /path -atime +number_#，理解中的是查找大于number_# + 1天的文件
                        if time.time() - f.stat().st_atime > atime_pattern + 86400:
                            atime_list.append(f)
                    except FileNotFoundError:
                        pass
                return atime_list

        elif atime_pattern[0][0] == "-":
            atime_pattern = int(atime_pattern[0][1:])
            atime_pattern = atime_pattern * 86400

            if file.is_dir():
                for f in file.rglob(name_pattern):
                    try: #find /path -atime 1number_#，理解中的是查找小于number_# + 1天的文件
                        if time.time() - f.stat().st_atime < atime_pattern + 86400:
                            #if f.is_dir():
                            #    continue
                            atime_list.append(f)
                    except FileNotFoundError:
                        pass
                    total += 1
                print(total)
                return atime_list

    def mtime(self):
        pass

    def ctime(self):
        pass

    def amin(self):
        pass

    def mmin(self):
        pass

    def cmin(self):
        pass

    def user(self):
        pass

    def group(self):
        pass

    def no_user(self):
        pass

    def no_group(self):
        pass

    def empty(self):
        pass

    def delete(self):
        pass


    def run(self,pattern):
        pattern_list = []
        run_command = self.command
        if getattr(self,run_command) == self.iname:
            pattern_list.append(pattern)
            pattern_list.append(pattern.upper())
        else:
            pattern_list.append(pattern)
        return getattr(self,run_command,lambda: print("{}  => not found".format(run_command)))(pattern_list)

if __name__ == '__main__':
    input_path = sys.argv[1]
    input_command = input("command: ").strip()
    input_pattern = input("pattern: ").strip()

    find = Find(input_path,input_command)
    try:
        for i in find.run(input_pattern):
            print(i)
    except TypeError:
        pass
import os
import time
import datetime

# print(os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    # время в минутах
    timeout = 100
    timedelta_timeout = datetime.timedelta(minutes=timeout)
    # путь к папке с файлами (формат файлов либо текстовый либо архивный)
    val1 = '/home/user/PythonProjects/Automation_03/val1_data_files/'
    # путь к папке с конфигами (файлы с расширением .cfg)
    val2 = '/home/user/PythonProjects/Automation_03/val2_config_files/'

    data_files_lst = os.listdir(val1)
    print(data_files_lst)
    for data_file in data_files_lst:
        data_file_path = f"{val1}{data_file}"
        print(f'Check file in directory: {data_file_path}')
        # check default.cfg  val2 #####################################################
        with open(f'{val2}default.cfg', 'r') as f:
            for line in f.readlines():
                stripped_line = line.rstrip('\n')
                file_name = f"{val1}{stripped_line}"
                print(f'in file {file_name}')
                if str(file_name) == str(data_file_path):
                    print("File detected in default.cfg")
                    abs_mod_time = time.ctime(os.path.getmtime(file_name))
                    abs_mod_datetime = datetime.datetime.strptime(abs_mod_time, "%a %b %d %H:%M:%S %Y")
                    dif_mod_time = datetime.datetime.now() - abs_mod_datetime
                    print(f"File modified {abs_mod_datetime} it's {dif_mod_time} ago.")
                    if dif_mod_time < timedelta_timeout:
                        print(f" File modified in {dif_mod_time}"
                              f" it's more than control period {timedelta_timeout}.")
                        break
                    else:
                        print(f'File was not modify in control period = {timedelta_timeout}')
                        break
                else:
                    pass
        # END check default.cfg #####################################################

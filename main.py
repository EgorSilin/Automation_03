import os
import time
import datetime

# print(os.path.dirname(os.path.abspath(__file__)))


def check_def_cfg(val1_inp, val2_inp, data_file_path_inp):
    """Func checking 1st condition"""
    # print(f'Check file in default.cfg')  # comment for prod
    file_in_def_cfg_key = False
    with open(f'{val2_inp}default.cfg', 'r') as f:
        for line in f.readlines():
            stripped_line = line.rstrip('\n')
            file_name = f"{val1_inp}{stripped_line}"
            # print(f'Check string in default.cfg {file_name}')  # comment for prod
            if str(file_name) == str(data_file_path_inp):
                # print("File detected in default.cfg")  # comment for prod
                file_in_def_cfg_key = True
                abs_mod_time = time.ctime(os.path.getmtime(file_name))
                abs_mod_datetime = datetime.datetime.strptime(abs_mod_time, "%a %b %d %H:%M:%S %Y")
                dif_mod_time = datetime.datetime.now() - abs_mod_datetime
                # print(f"File modified {abs_mod_datetime} it's {dif_mod_time} ago.")  # comment for prod
                if dif_mod_time < timedelta_timeout:
                    print(f"File '{file_name}' \nmodified at {abs_mod_datetime} ({dif_mod_time} ago)."
                          f" It's more than control period ({timedelta_timeout}).")
                    break
                else:
                    # print(f'File was not modify in control period = {timedelta_timeout}')  # comment for prod
                    break
    return file_in_def_cfg_key


if __name__ == '__main__':
    # время в минутах
    timeout = 100
    timedelta_timeout = datetime.timedelta(minutes=timeout)
    # путь к папке с файлами (формат файлов либо текстовый либо архивный)
    val1 = '/home/user/PythonProjects/Automation_03/val1_data_files/'
    # путь к папке с конфигами (файлы с расширением .cfg)
    val2 = '/home/user/PythonProjects/Automation_03/val2_config_files/'

    data_files_lst = sorted(os.listdir(val1))
    config_files_lst = sorted(os.listdir(val2))
    print(data_files_lst)
    print(config_files_lst)
    for data_file in data_files_lst:
        data_file_path = f"{val1}{data_file}"
        ################
        if not os.path.isfile(f'{data_file_path}'):
            # print(f'It is not file!')  # comment for prod
            continue
        ###################
        print(f'\nCheck file: {data_file_path}')
        is_in_def_cfg = check_def_cfg(val1, val2, data_file_path)
        print(f'KEY = {is_in_def_cfg}')
        # Check 2nd condition
        if not is_in_def_cfg:
            for config_file in config_files_lst:
                with open(f'{val2}{config_file}', 'r') as f:
                    pass



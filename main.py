import os
import time
import datetime
import binascii


def take_cfg_dict(val2_inp):
    """func build dict:
    {data_file_name_01: [cfg_file_path_01, cfg_file_path_02],
    data_file_name_02: [cfg_file_path_01, cfg_file_path_02]}"""
    cfg_dict_in_f = {}
    for config_file in config_files_lst:
        config_file_path = f"{val2_inp}{config_file}"
        if not os.path.isfile(f'{config_file_path}'):
            continue
        if config_file_path == f'{val2_inp}default.cfg':
            continue
        if os.path.splitext(config_file_path)[1] != '.cfg':
            continue
        with open(f'{val2_inp}{config_file}', 'r') as f:
            data_file_name = (f.readline()).rstrip('\n').lstrip('name:')
            print(data_file_name)
            print(f'XXX: {val2_inp}{config_file}')
            if data_file_name in cfg_dict_in_f:
                cfg_dict_in_f[data_file_name].append(f'{val2_inp}{config_file}')
            else:
                cfg_dict_in_f[data_file_name] = []
                cfg_dict_in_f[data_file_name].append(f'{val2_inp}{config_file}')
    return cfg_dict_in_f


def check_1st_cond(val1_inp, val2_inp, data_file_path_inp):
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
                          f" It's less than control period ({timedelta_timeout}).")  # comment for prod
                    break
                else:
                    print(f'File was not modify in control period = {timedelta_timeout}')
                    break
    return file_in_def_cfg_key


def check_2nd_cond(cfg_dict_inp, data_file_inp):
    # Check 2nd condition
    if data_file_inp in cfg_dict_inp:
        for cfg_path in cfg_dict_inp[data_file_inp]:
            print(f'Read config: {cfg_path}')  # comment for prod
            with open(cfg_path, 'r') as f:
                next(f)
                sig_list = []
                for cfg_line in f:
                    stripped_cfg_line = cfg_line.rstrip('\n')
                    sig_list.append(stripped_cfg_line)
                    # print(stripped_cfg_line)
                print(sig_list)
                sig_list_2 = [[sig_list[i], sig_list[i + 1]] for i in range(0, len(sig_list) - 1, 2)]
                print(sig_list_2)
                for sig in sig_list_2:
                    print(cfg_path)
                    print(sig[0])
                    print(sig[1])  # should be hex str
                    '''XXX = 585858, YYY = 595959, ZZZ = 5a5a5a'''
                    # hex_sig = binascii.hexlify(sig[1].encode('utf8'))  # from str to hex str
                    # print(hex_sig)
                    # unhex_sig = binascii.unhexlify(hex_sig).decode('utf8')  # from hex str to str
                    # print(unhex_sig)
                    print(data_file_path)
                    with open(data_file_path, 'rb') as ff:
                        file_bytes = ff.read()
                        file_hex = file_bytes.hex()
                        print(f'FILE IN BYTES: {file_bytes}, type: {type(file_bytes)}')  # comment for prod
                        print(f'FILE IN HEX: {file_hex}, type: {type(file_hex)}')  # comment for prod
                        if sig[1] in file_hex:
                            print(f"Alarm! Signature '{sig[1]} detected in {data_file_path}!'")


if __name__ == '__main__':
    # время в минутах
    timeout = 100
    timedelta_timeout = datetime.timedelta(minutes=timeout)
    # путь к папке с файлами (формат файлов либо текстовый либо архивный)
    # val1 = '/home/user/PythonProjects/Automation_03/val1_data_files/'
    val1 = '/home/user/PycharmProjects/Automation_03/val1_data_files/'
    # путь к папке с конфигами (файлы с расширением .cfg)
    # val2 = '/home/user/PythonProjects/Automation_03/val2_config_files/'
    val2 = '/home/user/PycharmProjects/Automation_03/val2_config_files/'

    data_files_lst = sorted(os.listdir(val1))
    config_files_lst = sorted(os.listdir(val2))
    cfg_dict = take_cfg_dict(val2)
    print(cfg_dict)
    print(data_files_lst)
    print(config_files_lst)
    for data_file in data_files_lst:
        data_file_path = f"{val1}{data_file}"
        print(f'\nCheck file: {data_file_path}')
        if not os.path.isfile(f'{data_file_path}'):
            # print(f'It is not file!')  # comment for prod
            continue
        is_in_def_cfg = check_1st_cond(val1, val2, data_file_path)
        print(f'KEY = {is_in_def_cfg}')
        if not is_in_def_cfg:
            check_2nd_cond(cfg_dict, data_file)

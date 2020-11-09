import os
import time
import datetime
import binascii
import csv


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
            if data_file_name in cfg_dict_in_f:
                cfg_dict_in_f[data_file_name].append(f'{val2_inp}{config_file}')
            else:
                cfg_dict_in_f[data_file_name] = []
                cfg_dict_in_f[data_file_name].append(f'{val2_inp}{config_file}')
    return cfg_dict_in_f


def write_to_cvs_top(file_name: str, cvs_str_inp: list):
    row_lst = []
    if os.path.isfile(f'{file_name}'):
        with open(file_name, mode='r', encoding='utf-8') as r_file:
            file_reader = csv.reader(r_file, delimiter=";")
            for row in file_reader:
                row_lst.append(row)
    with open(file_name, mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        file_writer.writerow([cvs_str_inp[0], cvs_str_inp[1], cvs_str_inp[2]])
        for row in row_lst:
            file_writer.writerow([row[0], row[1], row[2]])


def check_1st_cond(val1_inp, val2_inp, data_file_path_inp):
    """Func checking 1st condition"""
    # print(f'Checking 1st condition!')  # comment for prod
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
                    # print(f"Ok! File '{file_name}' \nmodified at {abs_mod_datetime} ({dif_mod_time} ago)."
                    #       f" It's less than control period ({timedelta_timeout}).")  # comment for prod
                    break
                else:
                    print(f"ALARM! File '{file_name}' has not been modified "
                          f"in control period = {timedelta_timeout}")
                    break
    return file_in_def_cfg_key


def check_2nd_cond(cfg_dict_inp, data_file_inp):
    """Func checking 2nd condition
    Signature samples: XXX = 585858, YYY = 595959, ZZZ = 5a5a5a"""
    # print(f'Checking 2nd condition!')
    if data_file_inp in cfg_dict_inp:
        # find cfg files for each data files
        for cfg_path in cfg_dict_inp[data_file_inp]:
            # print(f'Read config: {cfg_path}')  # comment for prod
            with open(cfg_path, 'r') as f:
                next(f)
                sig_list = []
                # scan cfg files to find timeout and signature
                for cfg_line in f:
                    stripped_cfg_line = cfg_line.rstrip('\n')
                    sig_list.append(stripped_cfg_line)
                sig_list_2 = [[sig_list[i], sig_list[i + 1]] for i in range(0, len(sig_list) - 1, 2)]
                # print(f"SIG 1xLIST: {sig_list}")
                # print(f"SIG 2xLIST: {sig_list_2}")
                for sig in sig_list_2:
                    if sig[0] == '0':
                        sig[0] = str(timeout)
                    # print(f"SIG '{sig[1]}' should be in {sig[0]} minutes")  # comment for prod

                    # module for ASCII signature
                    # hex_sig = binascii.hexlify(sig[1].encode('utf8'))  # from str to hex str
                    # print(hex_sig)
                    # unhex_sig = binascii.unhexlify(hex_sig).decode('utf8')  # from hex str to str
                    # print(unhex_sig)

                    # print(f"FILE PATH: {data_file_path}")  # comment for prod
                    with open(data_file_path, 'rb') as ff:
                        file_bytes = ff.read()
                        file_hex = file_bytes.hex()
                        # print(f'FILE IN BYTES: {file_bytes}, type: {type(file_bytes)}')  # comment for prod
                        # print(f'FILE IN HEX: {file_hex}, type: {type(file_hex)}')  # comment for prod
                        if sig[1] in file_hex:
                            # print(f"Ok! Signature '{sig[1]} detected in {data_file_path}!'")  # comment for prod
                            write_to_cvs_top("sig_det_log.csv", [datetime.datetime.now(),
                                                                 sig[1],
                                                                 data_file_path])
                        else:
                            # print(f"Signature '{sig[1]}' has not been detected "
                            #       f"in file '{data_file_path}' in this scan.")  # comment for prod
                            # check csv log file
                            with open("sig_det_log.csv", mode='r', encoding='utf-8') as r_file:
                                file_reader = csv.reader(r_file, delimiter=";")
                                count = 0
                                sig_in_log_key_in_check_period = True
                                for row in file_reader:
                                    count += 1
                                    row0_datetime = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")

                                    sig0_datetime = datetime.timedelta(minutes=int(sig[0]))
                                    dif_row0_datetime = datetime.datetime.now() - row0_datetime
                                    if row[1] == sig[1] and dif_row0_datetime <= sig0_datetime:
                                        # print(f"Signature {sig[1]} has been in log {dif_row0_datetime} ago "
                                        #       f"when check period {sig0_datetime}")  # comment for prod
                                        sig_in_log_key_in_check_period = True
                                        break
                                    else:
                                        sig_in_log_key_in_check_period = False
                                if not sig_in_log_key_in_check_period:
                                    print(f"ALARM! Signature {sig[1]} has not been in file "
                                          f"for the check period = {sig[0]}")
                                # print(f'Всего в файле {count} строк.')
    else:
        # print(f'File is not in config files.')  # comment for prod
        pass


if __name__ == '__main__':
    # время в минутах
    timeout = 16
    timedelta_timeout = datetime.timedelta(minutes=timeout)
    # путь к папке с файлами (формат файлов либо текстовый либо архивный)
    val1 = f'{os.path.dirname(os.path.abspath(__file__))}/val1_data_files/'
    # путь к папке с конфигами (файлы с расширением .cfg)
    val2 = f'{os.path.dirname(os.path.abspath(__file__))}/val2_config_files/'

    data_files_lst = sorted(os.listdir(val1))
    config_files_lst = sorted(os.listdir(val2))
    cfg_dict = take_cfg_dict(val2)
    # print(f'File in config dict: {cfg_dict}')  # comment for prod
    # print(f'Data files list: {data_files_lst}')  # comment for prod
    # print(f'Config file list: {config_files_lst}')  # comment for prod
    for data_file in data_files_lst:
        data_file_path = f"{val1}{data_file}"
        # print(f'\nCheck file: {data_file_path}')  # comment for prod
        if not os.path.isfile(f'{data_file_path}'):
            # print(f'It is not file!')  # comment for prod
            continue
        is_in_def_cfg = check_1st_cond(val1, val2, data_file_path)
        # print(f'Data file in default.cfg? {is_in_def_cfg}')  # comment for prod
        if not is_in_def_cfg:
            check_2nd_cond(cfg_dict, data_file)
        # FINISHED

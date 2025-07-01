# 使用netsh命令获取此电脑上所有网络适配器的IP地址（包括IPv4和IPv6），去除本地回环地址。

import subprocess
import locale
import ipaddress

system_encoding: str


def get_all_local_ip_v4():
    """
    获取本机IP地址
    :return: IP地址列表
    """
    ip_list = []
    cmd = "chcp 65001 >nul & netsh interface ipv4 show addresses"
    result = subprocess.check_output(cmd, shell=True).decode('utf-8')
    # print(result)
    for line in result.split('\n'):
        if 'IP Address' in line:
            ip_list.append(line.split(':')[1].strip())

    return ip_list


def get_all_local_ip_v6():
    """
    获取本机IPv6地址
    :return: IPv6地址列表
    """
    ip_list = []
    cmd = "chcp 65001 >nul & netsh interface ipv6 show addresses"
    result = subprocess.check_output(cmd, shell=True).decode('utf-8')
    # print(result)

    flag_line_is_address = 0
    for line in result.split('\n'):
        if 'Interface ' in line:
            flag_line_is_address = 0
        else:
            flag_line_is_address += 1
            if flag_line_is_address >= 4:
                if line.strip() == '':
                    # 空行结束
                    flag_line_is_address = -1
                    continue
                line_parts = []
                for part in line.split(sep=' '):
                    if not part:
                        continue
                    line_parts.append(part.strip())
                ip_list.append(line_parts[4].split('%')[0])

    return ip_list


def get_all_local_ip_v4_non_loopback():
    """
    获取本机IP地址（去除回环地址）
    :return: IP地址列表
    """
    ip_list = []
    cmd = "chcp 65001 >nul & netsh interface ipv4 show addresses"
    result = subprocess.check_output(cmd, shell=True).decode('utf-8')
    for line in result.split('\n'):
        if 'IP Address' in line:
            ip = line.split(':')[1].strip()
            if not ipaddress.ip_address(ip).is_loopback:
                ip_list.append(ip)

    return ip_list


def get_all_local_ip_v6_non_loopback():
    """
    获取本机IPv6地址（去除回环地址）
    :return: IPv6地址列表
    """
    ip_list = []
    cmd = "chcp 65001 >nul & netsh interface ipv6 show addresses"
    result = subprocess.check_output(cmd, shell=True).decode('utf-8')

    flag_line_is_address = 0
    for line in result.split('\n'):
        if 'Interface ' in line:
            flag_line_is_address = 0
        else:
            flag_line_is_address += 1
            if flag_line_is_address >= 4:
                if line.strip() == '':
                    # 空行结束
                    flag_line_is_address = -1
                    continue
                line_parts = []
                for part in line.split(sep=' '):
                    if not part:
                        continue
                    line_parts.append(part.strip())
                ip = line_parts[4].split('%')[0]
                if not ipaddress.ip_address(ip).is_loopback:
                    ip_list.append(ip)

    return ip_list


def get_all_local_ip_v4_non_local():
    """
    获取本机IP地址（去除本地地址）
    :return: IP地址列表
    """
    ip_list = []
    cmd = "chcp 65001 >nul & netsh interface ipv4 show addresses"
    result = subprocess.check_output(cmd, shell=True).decode('utf-8')
    for line in result.split('\n'):
        if 'IP Address' in line:
            # 使用ipaddress模块判断是否为本地地址
            ip = line.split(':')[1].strip()
            if not ipaddress.ip_address(ip).is_private:
                ip_list.append(ip)

    return ip_list


def get_all_local_ip_v6_non_local():
    """
    获取本机IPv6地址（去除本地地址）
    :return: IPv6地址列表
    """
    ip_list = []
    cmd = "chcp 65001 >nul & netsh interface ipv6 show addresses"
    result = subprocess.check_output(cmd, shell=True).decode('utf-8')

    flag_line_is_address = 0
    for line in result.split('\n'):
        if 'Interface ' in line:
            flag_line_is_address = 0
        else:
            flag_line_is_address += 1
            if flag_line_is_address >= 4:
                if line.strip() == '':
                    # 空行结束
                    flag_line_is_address = -1
                    continue
                line_parts = []
                for part in line.split(sep=' '):
                    if not part:
                        continue
                    line_parts.append(part.strip())
                ip = line_parts[4].split('%')[0]
                if not ipaddress.ip_address(ip).is_private:
                    ip_list.append(ip)

    return ip_list


if __name__ == '__main__':
    # 获取系统默认编码
    system_encoding = locale.getpreferredencoding()
    ip_list = get_all_local_ip_v4_non_loopback()
    print(ip_list)


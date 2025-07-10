# 使用netsh命令获取此电脑上所有网络适配器的IP地址（包括IPv4和IPv6），去除本地回环地址。

import subprocess
# import locale
import ipaddress

# system_encoding: str
import winreg
from typing import Dict, List, Tuple


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


def get_all_local_ip():
    """
    获取本机IP地址（包括IPv4和IPv6）
    :return: IP地址列表
    """
    ip_list = []
    ip_list.extend(get_all_local_ip_v4())
    ip_list.extend(get_all_local_ip_v6())
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


def get_all_local_ip_non_loopback():
    """
    获取本机IP地址（去除回环地址）
    :return: IP地址列表
    """
    ip_list = []
    ip_list.extend(get_all_local_ip_v4_non_loopback())
    ip_list.extend(get_all_local_ip_v6_non_loopback())
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


def get_all_local_ip_non_local():
    """
    获取本机IP地址（去除本地地址）
    :return: IP地址列表
    """
    ip_list = []
    ip_list.extend(get_all_local_ip_v4_non_local())
    ip_list.extend(get_all_local_ip_v6_non_local())
    return ip_list


def get_windows_proxy_settings() -> Tuple[Dict[str, str], List[str]]:
    try:
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path) as key:
            proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
            proxy_server, _ = winreg.QueryValueEx(key, "ProxyServer")
            proxy_override, _ = winreg.QueryValueEx(key, "ProxyOverride")

            proxies = {}
            if proxy_enable == 1 and proxy_server:
                if "=" in proxy_server:
                    # http=...;https=...
                    for part in proxy_server.split(";"):
                        proto, addr = part.split("=")
                        proxies[proto] = f"http://{addr}"
                else:
                    # 同一个代理给所有协议
                    proxies = {
                        "http": f"http://{proxy_server}",
                        "https": f"http://{proxy_server}"
                    }
            return proxies, proxy_override.split(";") if proxy_override else []
    except Exception as e:
        print("读取系统代理失败:", e)
    return {}, []


def host_matches_override(host, override_list):
    if not override_list:
        return False

    # 检查如果是短名（没有点），且有 <local>
    if '.' not in host:
        if "<local>" in override_list:
            return True

    # 检查通配符
    for pattern in override_list:
        pattern = pattern.lower()
        if pattern == "<local>":
            continue
        if pattern.startswith("*"):
            if host.endswith(pattern[1:]):
                return True
        elif host == pattern:
            return True
    return False


if __name__ == '__main__':
    # 获取系统默认编码
    # system_encoding = locale.getpreferredencoding()
    ip_list = get_all_local_ip_v4_non_local()
    print(ip_list)


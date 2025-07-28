import sys
import os.path as osp

build_flag: bool
author_name = 'LiuJiewenTT'
author_email = 'liuljwtt@163.com'
author_info: dict
project_name = 'DynamicIP2CF'
project_link = 'https://github.com/LiuJiewenTT/DynamicIP2CF'
product_check_update_url = 'https://api.github.com/repos/LiuJiewenTT/DynamicIP2CF/releases/latest'
product_name = 'CloudFlare Dynamic IP Updater'
program_name = 'DynamicIP2CF'
product_version = (0, 0, 1, 0)
program_version = (0, 0, 1, 0)
program_version_str: str
program_iconpicture_paths = [
    'res/assets/icon.png',
]
program_iconpicture_idx: int # = 0
program_iconpicture_path: str
frontend_name = 'CloudFlare Dynamic IP Updater'
license_type = ''
buildin_exinfo: object
programinfo_str1: str
programinfo_html_str1: str


# 以下自动生成
author_info = {
    'author_name': author_name,
    'author_email': author_email
}

if not osp.exists(__file__) and getattr(sys, 'frozen', False):
    build_flag = True
else:
    build_flag = False

if build_flag is True:
    # from ...keep_local.build import builtin_exinfo
    from .builtin_exinfo import Builtin_ExInfo
else:
    from .builtin_exinfo_default import Builtin_ExInfo
builtin_exinfo: Builtin_ExInfo


def override_programinfo_vars(self):
    global program_iconpicture_idx
    if self.program_iconpicture_idx is not None:
        program_iconpicture_idx = self.program_iconpicture_idx
    else:
        program_iconpicture_idx = 0


def ver2str(version_tuple: tuple):
    version_str = 'v'
    for i in version_tuple:
        version_str += f'{i}.'
    version_str = version_str[:-1].rstrip('.0')
    return version_str


def init_program_info():
    global builtin_exinfo, product_version_str, program_version_str, program_iconpicture_path, \
        programinfo_str1, programinfo_html_str1

    builtin_exinfo = Builtin_ExInfo()

    override_programinfo_vars(builtin_exinfo)
    product_version_str = ver2str(product_version)
    program_version_str = ver2str(program_version)
    program_iconpicture_path = program_iconpicture_paths[program_iconpicture_idx]

    programinfo_str1 = (f'Product Name: {product_name}\n'
                        f'FrontEnd Name: {frontend_name}\n'
                        f'Author: {author_name} <{author_email}>\n'
                        f'Program Version: {program_version_str}\n'
                        f'Project Name: {project_name}\n'
                        f'Project Link: {project_link}\n'
                        f'License Type: {license_type}\n'
                        f'{builtin_exinfo.summary_str_singleline()}\n')

    programinfo_html_str1 = (f'Product Name: {product_name}<br>\n'
                             f'FrontEnd Name: {frontend_name}<br>\n'
                             f'Author: {author_name} &lt;<a href="mailto:{author_email}">{author_email}</a>&gt;<br>\n'
                             f'Program Version: {program_version_str}<br>\n'
                             f'Project Name: {project_name}<br>\n'
                             f'Project Link: <a href="{project_link}">{project_link}</a><br>\n'
                             f'License Type: {license_type}<br>\n'
                             f'{builtin_exinfo.summary_str_singleline()}<br>\n')


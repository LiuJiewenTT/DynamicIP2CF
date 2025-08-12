import os
import os.path as osp
import sys
import datetime

from DynamicIP2CF import programinfo

import PyInstaller
import PyInstaller.__main__ as pyi_main
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT, MERGE, Splash


build_root_path = osp.dirname(osp.abspath(__file__))
project_root_path = osp.dirname(osp.dirname(build_root_path))

src_path = osp.join(project_root_path, 'src')
res_path = osp.join(project_root_path, 'res')

dist_path = osp.join(build_root_path, 'dist')         # 打包输出目录
work_path = osp.join(build_root_path, 'build')        # 打包临时目录
specs_path = osp.join(build_root_path, 'specs')        # 打包配置文件目录
runtime_hooks_path = osp.join(build_root_path, 'runtime_hooks')  # 运行时钩子目录

# 自定义缓存目录
my_build_cache_path = osp.join(build_root_path, 'my_build_cache')

print(f'build_root_path: {build_root_path}')
print(f'project_root_path: {project_root_path}')
print(f'src_path: {src_path}')
print(f'res_path: {res_path}')
print(f'dist_path: {dist_path}')
print(f'work_path: {work_path}')
print(f'specs_path: {specs_path}')
print(f'runtime_hooks_path: {runtime_hooks_path}')
print(f'my_build_cache_path: {my_build_cache_path}')

main_file = f'{src_path}/DynamicIP2CF/main.py'
gui_main_file = f'{src_path}/DynamicIP2CF/gui/main.py'
icon_file = f'{res_path}/assets/icons/icon.ico'


spec_startups: dict # 中转构建配置


builtin_exinfo: object


def generate_builtin_exinfo(edition_str: str):
    global builtin_exinfo

    build_time = datetime.datetime.now().astimezone()
    build_timestamp = build_time.timestamp()
    # build_timestamp_str = str(build_time)
    build_timestamp_str = build_time.strftime('%Y-%m-%d %H:%M:%S.%f %z(%Z) %j/%V:%u/%a')

    builtin_exinfo_content = ""

    value_map = {
        'edition_str': edition_str,
        'build_timestamp': build_timestamp,
        'build_timestamp_str': build_timestamp_str,
        'hasSplash': False,
        'program_iconpicture_idx': 0
    }
    with open(osp.join(build_root_path, "builtin_exinfo_template.py"), "r", encoding="utf-8") as f1:
        builtin_exinfo_template_content = f1.read()
        builtin_exinfo_content = builtin_exinfo_template_content.format_map(value_map)
        if not osp.exists(my_build_cache_path):
            os.makedirs(my_build_cache_path)
        with open(osp.join(my_build_cache_path, "builtin_exinfo.py"), "w", encoding="utf-8") as f2:
            f2.write(builtin_exinfo_content)
    builtin_exinfo = (f"{programinfo.__package__}.builtin_exinfo", osp.join(my_build_cache_path, "builtin_exinfo.py"), 'PYMODULE')
    return builtin_exinfo


qt_wanted_list = [
    'qicns.dll',
    'qminimal.dll',
    'qjpeg.dll',
    'qwindows.dll',
    'QtGui',
    'QtNetwork',
    'QtCore',
    'QtWidgets',
    'Qt6Core',
    'Qt6Gui',
    'Qt6Network',
    'Qt6Widgets',
    'pyside6.abi',
    'styles'
]


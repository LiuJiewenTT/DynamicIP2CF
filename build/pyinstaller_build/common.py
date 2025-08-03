import os.path as osp

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

print(f'build_root_path: {build_root_path}')
print(f'project_root_path: {project_root_path}')
print(f'src_path: {src_path}')
print(f'res_path: {res_path}')
print(f'dist_path: {dist_path}')
print(f'work_path: {work_path}')
print(f'specs_path: {specs_path}')

main_file = f'{src_path}/DynamicIP2CF/main.py'
gui_main_file = f'{src_path}/DynamicIP2CF/gui/main.py'
icon_file = f'{res_path}/assets/icons/icon.ico'


spec_startups: dict # 中转构建配置



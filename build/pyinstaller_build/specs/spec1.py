# from DynamicIP2CF import programinfo
# from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT, MERGE, Splash
from typing import Union
__package__ = 'pyinstaller_build.specs'

from .. import common
from ..common import *


hiddenimports = []
# hiddenimports = ['_pyi_rth_utils']

# runtime_hooks = []
runtime_hooks = [osp.join(runtime_hooks_path, 'main_hook.py')]


def assemble(flag_onefile: bool, a: Analysis, pyz: PYZ) -> Union[EXE, COLLECT]:
    common_kwargs = {
        'name': programinfo.program_name,
        'icon': icon_file,
        'upx': True,
        'upx_exclude': [],
        'strip': False
    }
    exe_kwargs = {
        **common_kwargs,
        'debug': False,
        'bootloader_ignore_signals': False
    }
    collect_kwargs = {
        **common_kwargs
    }
    collect_kwargs.update({
        'name': programinfo.product_name
    })

    if flag_onefile:
        exe_vargs = [
            a.scripts,
            a.binaries,
            a.dependencies,
            a.datas,
            a.hiddenimports,
        ]
        return EXE(pyz, *exe_vargs, **exe_kwargs)
    else:
        exe_kwargs.update({
            'exclude_binaries': True
        })
        exe_vargs = [
            a.scripts,
            a.dependencies,
        ]
        collect_vargs = [
            a.binaries,
            a.datas,
        ]
        exe = EXE(pyz, *exe_vargs, **exe_kwargs)
        return COLLECT(exe, *collect_vargs, **collect_kwargs)


analysed_files = Analysis([main_file],
                          pathex=[],
                          hiddenimports=hiddenimports,
                          binaries=[],
                          datas=[
                              (osp.join(res_path, 'assets'), osp.join('res', 'assets'))
                          ],
                          hookspath=[],
                          hooksconfig={},
                          runtime_hooks=runtime_hooks,
                          excludes=[],
                          noarchive=False,
                          optimize=0,
                          )

temp_list = []
for i in range(analysed_files.binaries.__len__()):
    item = analysed_files.binaries[i]
    if item[0].startswith('PySide6'):
        print(item, end='')
        temp_flag = False
        for wanted_item in common.qt_wanted_list:
            if wanted_item in item[0]:
                temp_flag = True
                break
        if not temp_flag:
            print(' removed')
        else:
            temp_list.append(item)
            print()
    else:
        temp_list.append(item)
analysed_files.binaries = temp_list

temp_list = []
for i in range(analysed_files.datas.__len__()):
    item = analysed_files.datas[i]
    if item[0].startswith('PySide6'):
        print(item, end='')
        temp_flag = False
        if item[0].endswith('.qm'):
            print(' removed')
        else:
            temp_list.append(item)
            print()
    else:
        temp_list.append(item)
analysed_files.datas = temp_list

analysed_files.pure.append(common.generate_builtin_exinfo('Release'))
pyz = PYZ(analysed_files.pure)
flag_onefile = common.spec_startups.get('onefile', False)
result = assemble(flag_onefile, analysed_files, pyz)
# return result




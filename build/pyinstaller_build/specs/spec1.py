# from DynamicIP2CF import programinfo
# from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT, MERGE, Splash
from typing import Union
__package__ = 'pyinstaller_build.specs'

from .. import common
from ..common import *

# hiddenimports = []
hiddenimports = ['_pyi_rth_utils', 'pyi_rth_pyside6']


def assemble(flag_onefile: bool, a: Analysis, pyz: PYZ) -> Union[EXE, COLLECT]:
    common_kwargs = {
        'name': programinfo.program_name,
        'icon': icon_file,
        'upx': True,
        'upx_exclude': [],
        'runtime_tmpdir': None,
    }
    exe_kwargs = {
        **common_kwargs
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


analysed_files = Analysis([main_file], pathex=[], hiddenimports=hiddenimports)
pyz = PYZ(toc=analysed_files)
flag_onefile = common.spec_startups.get('onefile', False)
result = assemble(flag_onefile, analysed_files, pyz)
# return result




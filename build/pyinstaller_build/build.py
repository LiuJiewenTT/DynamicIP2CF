__package__ = 'pyinstaller_build'
from . import common
from .common import *

spec_file = osp.join(specs_path, 'spec1.py')
flag_clean_build = True
flag_clean_build = False

common.spec_startups = {
    'onefile': False
}


if __name__ == '__main__':
    pyi_config = None
    pyi_main.run_build(pyi_config, noconfirm=True, spec_file=spec_file, distpath=dist_path, workpath=work_path, clean_build=flag_clean_build)


import os
from DynamicIP2CF import common_static

RES_PATH_NAME: str =  '{}_RES_PATH'.format(common_static.program_name.upper())
RES_PATH: str = os.path.join(os.path.dirname(__file__), 'res')
os.environ[RES_PATH_NAME] = RES_PATH
# print('{}: {}'.format(RES_PATH_NAME, RES_PATH))

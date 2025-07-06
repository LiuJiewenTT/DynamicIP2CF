import os
from DynamicIP2CF import common_static


class EnvVarManager:

    separator: str

    def __init__(self):
        if os.name == 'nt':
            self.separator = ';'
        else:
            self.separator = ':'

    # 拆分环境变量列表
    def split_env_var(self, env_var: str):
        return env_var.split(self.separator)


class ResourceManager:

    res_root: str

    def __init__(self):
        self.env_var_manager = EnvVarManager()
        self.res_root = os.getenv("{}_RES_PATH".format(common_static.program_name.upper()))
        if not self.res_root:
            python_paths = self.env_var_manager.split_env_var(os.getenv('PYTHONPATH'))
            # print(python_paths)
            for path in python_paths:
                if path.endswith(os.sep + "res"):
                    self.res_root = path
                    break
        if not self.res_root:
            raise Exception("Resource root path not set. Please set {}_RES_PATH environment variable.".format(common_static.program_name.upper()))
        # print("Resource root path: {}".format(self.res_root))

    def get_res_path(self, path: str):
        print("get_res_path: {}".format(path))
        print("res_path: {}".format(os.path.join(self.res_root, path.replace('/', os.sep))))
        return os.path.join(self.res_root, path.replace('/', os.sep))
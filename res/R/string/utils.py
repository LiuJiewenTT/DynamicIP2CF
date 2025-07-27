import argparse


class Namespace(argparse.Namespace.__base__):
    """Simple object for storing attributes.

    Implements equality by attribute names and values, and provides a simple
    string representation.

    Base class is argparse._AttributeHolder
    """

    def __init__(self, **kwargs):
        for name in kwargs:
            value = kwargs[name]
            if isinstance(value, dict):
                value = Namespace(**value)
            setattr(self, name, value)

    def __eq__(self, other):
        if not isinstance(other, Namespace):
            return NotImplemented
        return vars(self) == vars(other)

    def __contains__(self, key: str):
        if key in self.__dict__:
            return True
        retv = False
        sub_key = (key.split('.', 1) + [''])[1]
        if not sub_key:
            return False
        for value in self.__dict__.values():
            if isinstance(value, Namespace):
                retv = sub_key in value
                if retv:
                    break
        return retv

    def _get_kwargs_pure(self):
        items = super()._get_kwargs()
        items = {k: v if not isinstance(v, Namespace) else v._get_kwargs_pure() for k, v in items}
        return items

    def flatten(self, d, parent_key='', sep='.') -> dict:
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                items.extend(self.flatten(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def toHintClassStr(self, class_dict=None, tab_depth=0):
        class_str = ''
        tab_str = '    '
        tabs_str = tab_str * tab_depth
        if class_dict is None:
            class_dict = self._get_kwargs_pure()
        for k, v in class_dict.items():
            if isinstance(v, dict):
                v = self.toHintClassStr(v, tab_depth + 1)
                class_str += "%sclass %s: \n%s" % (tabs_str, k, v)
                # print('-'*50 + '\n' + class_str + '\n' + '-'*50 + '\n')
            else:
                class_str += '%s%s: %s\n' % (tabs_str, k, type(v).__name__)
                # print('-'*50 + '\n' + class_str + '\n' + '-'*50 + '\n')
        return class_str

    def __str__(self, format_spec='dict', json_options=None, yaml_options=None, xml_options=None):
        items = self._get_kwargs_pure()
        # print(items)
        if json_options is None:
            json_options = {
                'indent': 2,
                'ensure_ascii': False
            }
        if yaml_options is None:
            yaml_options = {
                'default_flow_style': False,
                'allow_unicode': True
            }
        if xml_options is None:
            xml_options = {
                'pretty': True
            }

        if format_spec == 'json':
            import json
            return json.dumps(items, **json_options)
        elif format_spec == 'yaml':
            import yaml
            return yaml.dump(items, **yaml_options)
        elif format_spec == 'toml':
            import toml
            return toml.dumps(items)
        elif format_spec == 'ini':
            import configparser
            import io
            config = configparser.ConfigParser()
            config.read_dict(items)
            output = io.StringIO()
            config.write(output)
            return output.getvalue()
        elif format_spec == 'xml':
            import xmltodict
            return xmltodict.unparse({'root': items}, **xml_options)
        elif format_spec == 'flattened':
            return '\n'.join(['%s=%s' % (k, v) for k, v in self.flatten(items).items()])
        elif format_spec == 'dict':
            return str(items)
        elif format_spec == 'repr':
            return self.__repr__()
        else:
            raise ValueError('Unsupported format specifier: %s' % format_spec)

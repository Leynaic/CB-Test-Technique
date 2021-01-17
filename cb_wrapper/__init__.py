# -*- coding: utf-8 -*-
import yaml
import json


class APIModern:
    def __init__(self):
        self.files = {}
        self.config = self._load_config()

        if self.config.get('api_key') is None:
            raise Exception('An API Key must be defined in the configuration file.')

    @staticmethod
    def _load_config():
        """
        Load configuration from config.yaml
        :return: The config dictionary from the file
        """
        try:
            with open('config.yaml', 'r') as config_file:
                config = yaml.load(config_file, Loader=yaml.FullLoader)
                return config if config is not None else {}
        except FileNotFoundError:
            return {}

    def translate(self, target, files):
        """
        Call all functions to proceed with the translation
        :param target: The target language
        :param files: The list of files to translate
        :return:
        """
        if not isinstance(files, (str, list, tuple)):
            raise TypeError("Files must be a string or a list.")

        # Cast files params to list of files path
        files = [files] if isinstance(files, str) else files

        # Read all files to save their content
        self.read_files(files)
        self._prepare_for_api()

    def read_files(self, files):
        """
        Read each files to extract their content into dictionaries
        :param files: The list of files to read
        :return:
        """
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as json_content:
                    self.files[file] = {
                        'content': json.load(json_content)
                    }
            except FileNotFoundError:
                raise FileNotFoundError("The provided JSON file path is not correct.")

    def _prepare_for_api(self):
        """
        For each files get the list of string from the json
        :return:
        """
        for key, data in self.files.items():
            self.files[key] = self.json_to_str(data)
            self.files[key] = self.str_to_json(data)

    @staticmethod
    def json_to_str(data):
        """
        Parse json to string list
        :param data: The data of file
        :return: The new parsed data
        """
        result = []

        def insert_value(value, add_double_points):
            # If value is object
            if type(value) is dict:
                if add_double_points:
                    result.append(':{')
                else:
                    result.append('{')
                flat(value)
                result.append('},')
            # If value is an array
            elif type(value) is list:
                if add_double_points:
                    result.append(':[')
                else:
                    result.append('[')
                flat(value)
                result.append('],')
            # Else the value is a string
            else:
                result.append(':')
                result.append(str(value))
                result.append(',')

        def flat(_content):
            # If content is an array
            if type(_content) is list:
                for value in _content:
                    insert_value(value, False)
            # Else content is an object
            else:
                for key, value in _content.items():
                    # Append key associated to the value
                    result.append(key)
                    insert_value(value, True)

        result.append('{' if type(data['content']) is dict else '[')
        flat(data['content'])
        result.append('}' if type(data['content']) is dict else ']')

        data['content'] = result

        return data

    @staticmethod
    def str_to_json(data):
        """
        Build the json from the string list
        :param data: The data
        :return:
        """
        result = ""
        for content in data['content']:
            if content in (':{', '{', '},', '}', ':[', '[', ']', '],', ':', ','):
                result += content
            else:
                result += '"' + content + '"'

        replace_dict = ((',}', '}'), (',]', ']'), ('\r', ''), ('\n', ''), (',:', ','), ('[:', '['))
        for char_from, char_to in replace_dict:
            result = result.replace(char_from, char_to)

        data['content'] = json.loads(result)

        return data


"""
        replace_dict = (
            ('{"}', '{}'), ('["]', '[]'), (',"],"}', ']}'), ('["{', '[{'),
            (',"]', '],'), (',"[', ',['), ('],"]', ']]'), ('},]', '}]'),
            ('},"{', '}, {'), ('{"{', '{{'), (',,', ','), ('},}', '}}')
        )
        for from_char, to_char in replace_dict:
            new_json = new_json.replace(from_char, to_char)
"""
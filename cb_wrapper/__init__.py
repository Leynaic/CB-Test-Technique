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

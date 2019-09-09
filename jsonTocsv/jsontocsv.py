import json
import csv
from zipfile import ZipFile
import os

class JsonToCsv:

    def __init__(self, obj, out_path):
        '''

        :param obj: The Json object that needs to be parser to CSV format
        :param out_path: The Path where CSV file have to be writer

        '''

        tree = self.get_tree(obj)
        if isinstance(obj, list):
            header = [i[0] for i in tree[0]]
        else:
            header = [i[0] for i in tree]
        self.render_csv(header, tree, out_path)

    def is_dict(self, item, ans=[]):
        '''

        :param item: Receive a list of dict or one dict
        :param ans: empty list using to store dict elements
        :return: The tree of json elements
        '''
        tree = []
        for k,v in item.items():

            if isinstance(v,dict):
                ans.append(str(k))
                tree.extend(self.is_dict(v, ans))
                ans=[]

            elif isinstance(v, list):
                ans.append(str(k))
                tree.extend(self.is_dict(v[0], ans))
                ans = []

            else:

                if ans:
                    ans.append(str(k))
                    key = ','.join(ans).replace(',','.')
                    tree.extend([(key, str(v))])
                    ans.remove(str(k))
                else:
                    tree.extend([(str(k),str(v))])
        return tree

    def is_json(self, myjson):
        try:
            json_object = json.loads(myjson)
        except (ValueError,TypeError) as e:
            return False
        return True

    def get_tree(self, item):
        '''

        :param item: The JSON structure submitted to be parsed
        :return: The tree of json elements
        '''
        tree = []
        if isinstance(item, dict):
            tree.extend(self.is_dict(item, ans=[]))
            return tree
        elif isinstance(item, list):
            tree = []
            for i in item:
                if self.is_json(i) == True:
                    i = json.loads(i)
                tree.append(self.get_tree(i))
            return tree
        elif isinstance(item, str):
            if self.is_json(item) == True:
                item = json.loads(item)
                tree.extend(self.is_dict(item, ans=[]))
                return tree
        else:
            tree.extend([(key, item)])
        return tree

    def render_csv(self, header, data, filenamedir):
        '''
        :param header: The CSV file header
        :param data: the csv data
        :param out_path: The path where the file should be created
        :return: None

        '''
        if not os.path.exists(filenamedir):
            os.makedirs(filenamedir)
        input = []
        with open(filenamedir, 'w') as f:
            dict_writer = csv.DictWriter(f, fieldnames=header)
            dict_writer.writeheader()
            if not isinstance(data[0],list):
                input.append(dict(data))
            else:
                for i in data:
                    input.append(dict(i))
            dict_writer.writerows(input)
        return filenamedir

    def get_all_file_paths(self, directory):
        '''
        :param directory: The directory where the csv files are stored
        :return: One list of files and path
        '''

        file_paths = []

        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
        return file_paths

    def zipfile(self, path, filename):
        '''
        :param path: The directory where the files are stored
        :param filename: The name of zip file
        :return: The file path and the name of zip file
        '''
        if not os.path.exists(path):
            os.makedirs(path)
        self.directory = path
        file_paths = self.get_all_file_paths(self.directory)
        for file_name in file_paths:
            print(file_name)
        with ZipFile(filename, 'w') as zip:
            for file in file_paths:
                zip.write(file)
        return filename
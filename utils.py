from enum import Enum

from segeval.data import load_nested_folders_dict, input_linear_mass_json
from segeval.data.jsonutils import output_linear_mass_json


class LoadTypeEnum(Enum):
    fold = 0,
    json = 1


def load_dataset(path, load_type=LoadTypeEnum.fold):
    """
    Load data according to load type.
    :param path: file path or file fold path
    :param load_type: fold or json (LoadTypeEnum)
    :return: dataset
    """
    if load_type == LoadTypeEnum.fold:
        return load_nested_folders_dict(path, filetype="tsv")
    else:
        return input_linear_mass_json(path)


def write_dataset(dataset, file_path="./data/dataset.json"):
    """
    Write dataset.
    :param dataset: dataset
    :param file_path: des file path
    :return: None
    """
    output_linear_mass_json(file_path, dataset)

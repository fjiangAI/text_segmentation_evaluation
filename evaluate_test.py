from segeval.data import Dataset

from evaluate import Evaluate
from utils import write_dataset, load_dataset, LoadTypeEnum


def write_dataset_example():
    """
    An example for writing dataset.
    :return: None
    """
    gold = [2, 3, 6]
    h = [5, 6]
    gold_dataset = Dataset(
        {'test1':
             {'golden': gold,
              },
         'test2':
             {'golden': gold,
              },
         })
    test_dataset = Dataset(
        {'test1':
             {'test': h,
              },
         'test2':
             {'test': h,
              },
         })
    write_dataset(gold_dataset, "./data/golden.json")
    write_dataset(test_dataset, "./data/test.json")


def load_dataset_example(method=1):
    """
    An example for loading dataset.
    :param method: 1 (by fold including tsv files) or 2 (by json)
    :return: gold_dataset, test_dataset
    """
    # method 1: load by file fold
    if method == 1:
        gold_dataset = load_dataset(path="./data/golden", load_type=LoadTypeEnum.fold)
        test_dataset = load_dataset(path="./data/test", load_type=LoadTypeEnum.fold)
    else:
        gold_dataset = load_dataset(path="./data/golden.json", load_type=LoadTypeEnum.json)
        test_dataset = load_dataset(path="./data/test.json", load_type=LoadTypeEnum.json)
    return gold_dataset, test_dataset


if __name__ == '__main__':
    for i in range(1, 3):
        print("方法" + str(i))
        gold_dataset, test_dataset = load_dataset_example(method=i)
        evaluate = Evaluate()
        evaluate.calculate_results(test_dataset, gold_dataset)
        print(evaluate.to_string())

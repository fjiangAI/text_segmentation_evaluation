import os

from seg_file import SegFile


class MainExec:
    def __init__(self):
        self.gold_lines = []
        self.predict_lines = []
        self.seg_file_list = []

    def convert_file(self, golden_file, predict_file):
        """
        Convert result from golden and predict file.
        :param golden_file: the golden file name
        :param predict_file: the predict file name
        :return: None
        """
        with open(golden_file, encoding='utf-8', mode='r') as fr:
            self.gold_lines = fr.readlines()
        with open(predict_file, encoding='utf-8', mode='r') as fr:
            self.predict_lines = fr.readlines()
        self.__convert_file()

    def write_to_file(self, des_path, data_type="golden"):
        """
        Write result to file.
        :param des_path: the des file path
        :param data_type: str "golden" or "test"
        :return:
        """
        if os.path.exists(des_path):
            pass
        else:
            os.mkdir(des_path)
        for seg_file in self.seg_file_list:
            seg_file.convert_seq_to_mass(data_type)
            if len(seg_file.golden_masses) < 2:
                continue
            seg_file.write_to_file(des_path + "/" + seg_file.file_name + ".tsv", data_type)

    def write_to_file_for_parsing(self, des_file, data_type="test"):
        """
        Write the result to file for parsing.
        :param des_file:
        :param data_type:
        :return:
        """
        with open(des_file, encoding='utf-8', mode='w') as fw:
            for seg_file in self.seg_file_list:
                temp_string = seg_file.for_parsing_to_string(data_type=data_type)
                fw.write(temp_string + "\n")

    def __convert_file(self):
        # TODO convert predict and golden file to seg file.
        pass


if __name__ == '__main__':
    main_exec = MainExec()
    root = "./model_type/"
    main_exec.convert_file(golden_file=root + "golden_file.tsv", predict_file=root + "predict_file.txt")
    main_exec.write_to_file(des_path=root + "golden", data_type="golden")
    main_exec.write_to_file(des_path=root + "test", data_type="test")
    main_exec.write_to_file_for_parsing(des_file=root + "model_type_predict_boundary.txt", data_type="test")

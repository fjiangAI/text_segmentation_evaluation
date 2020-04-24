class SegFile:
    """
    The file, that contains seg sequence, will be saved.
    """
    def __init__(self, file_name, golden_seg_seg, predict_seg_seq):
        self.file_name = file_name
        self.golden_seg_seq = golden_seg_seg
        self.golden_masses = []
        self.predict_seg_seq = predict_seg_seq
        self.predict_masses = []

    def write_to_file(self, des_file, data_type="golden"):
        """
        Write the result to file.

        The write example :
        coder_type
        golden	6	4	3

        :param des_file: The file name that you want to save it into.
        :param data_type: str "golden" or "test"
        :return: None
        """
        if data_type == "golden":
            with open(des_file, encoding='utf-8', mode='w') as fw:
                fw.writelines("coder_type\n")
                fw.write(data_type)
                for mass in self.golden_masses:
                    fw.write("\t" + str(mass))
                fw.write("\n")
        else:
            with open(des_file, encoding='utf-8', mode='w') as fw:
                fw.writelines("coder_type\n")
                fw.write(data_type)
                for mass in self.predict_masses:
                    fw.write("\t" + str(mass))
                fw.write("\n")

    def convert_seq_to_mass(self, data_type="golden"):
        """
        Convert seg sequence to mass.
        :param data_type: str "golden" or "test"
        :return: None
        """
        if data_type == "golden":
            curr_step = 1
            for label in self.golden_seg_seq:
                if label == "0":
                    curr_step += 1
                else:
                    self.golden_masses.append(curr_step)
                    curr_step = 1
            self.golden_masses.append(curr_step)
        else:
            curr_step = 1
            for label in self.predict_seg_seq:
                if label == "0":
                    curr_step += 1
                else:
                    self.predict_masses.append(curr_step)
                    curr_step = 1
            self.predict_masses.append(curr_step)

    def for_parsing_to_string(self, data_type="test"):
        """
        Get the string of result for parsing.
        :param data_type: "test" or "golden"
        :return: str
        """
        result = self.file_name
        if data_type == "test":
            for seq in self.predict_seg_seq:
                result = result + "\t" + seq
        result = result + "\t1"
        return result
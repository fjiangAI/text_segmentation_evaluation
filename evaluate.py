from enum import Enum

from segeval.window.pk import pk
from segeval.window.windowdiff import window_diff as WD
from segeval.similarity.boundary import boundary_similarity as B
from segeval.similarity.segmentation import segmentation_similarity as S


class CalculateEnum(Enum):
    """
    Four indicates: pk,windiff,boundary_similarity,segmentation_similarity.
    """
    pk = 0
    windiff = 1
    boundary_similarity = 2,
    segmentation_similarity = 3,


class Evaluate:
    """
    This class is to evaluate two dataset text segmentation by four indicates.
    """

    def __init__(self):
        self.pk_to_weight = []
        self.windiff_to_weight = []
        self.B_to_weight = []
        self.S_to_weight = []
        self.calculator_dict = {
            CalculateEnum.pk: pk,
            CalculateEnum.windiff: WD,
            CalculateEnum.boundary_similarity: B,
            CalculateEnum.segmentation_similarity: S,
        }
        self.weight_dict = {
            CalculateEnum.pk: self.pk_to_weight,
            CalculateEnum.windiff: self.windiff_to_weight,
            CalculateEnum.boundary_similarity: self.B_to_weight,
            CalculateEnum.segmentation_similarity: self.S_to_weight,
        }
        self.pk_value = -1
        self.windiff_value = -1
        self.segmentation_similarity_value = -1
        self.boundary_similarity_value = -1

    def calculate_results(self, h_dataset, gold_dataset, window_size=-1):
        """
        Calculate four indicates.
        :param h_dataset: test_dataset
        :param gold_dataset: gold_dataset
        :param window_size: optional
        :return: pk_value, windiff_value, segmentation_similarity_value, boundary_similarity_value
        """
        self._calculate(h_dataset, gold_dataset, window_size, calc_type=CalculateEnum.pk)
        self.pk_value = self._get_result(calc_type=CalculateEnum.pk)

        self._calculate(h_dataset, gold_dataset, window_size, calc_type=CalculateEnum.windiff)
        self.windiff_value = self._get_result(calc_type=CalculateEnum.windiff)

        self._calculate(h_dataset, gold_dataset, window_size, calc_type=CalculateEnum.boundary_similarity)
        self.boundary_similarity_value = self._get_result(calc_type=CalculateEnum.boundary_similarity)

        self._calculate(h_dataset, gold_dataset, window_size, calc_type=CalculateEnum.segmentation_similarity)
        self.segmentation_similarity_value = self._get_result(calc_type=CalculateEnum.segmentation_similarity)

        return self.pk_value, self.windiff_value, self.segmentation_similarity_value, self.boundary_similarity_value

    def to_string(self):
        """
        To show the result.
        :return: str
        """
        one_minus_pk = 1 - self.pk_value
        one_minus_windiff = 1 - self.windiff_value
        result_string = ("1-pk:%.3f\t1-WD:%.3f\tS:%.3f\tB:%.3f" % (
            one_minus_pk, one_minus_windiff, self.segmentation_similarity_value, self.boundary_similarity_value))
        return result_string

    def _get_result(self, calc_type=CalculateEnum.pk):
        """
        Get the result by the type of calculator.
        :param calc_type: pk, windiff,boundary_similarity or segmentation_similarity
        :return: the output value of calculator
        """
        result_value = sum([pw[0] * pw[1] for pw in self.weight_dict[calc_type]]) / sum(
            [pw[1] for pw in self.weight_dict[calc_type]]) if len(
            self.weight_dict[calc_type]) > 0 else -1.0
        return result_value

    def _calculate(self, h_dataset, gold_dataset, window_size=-1, calc_type=CalculateEnum.pk):
        """
        :param calc_type: the type of calculator
        :param gold_dataset: gold segmentation
        :param h_dataset: hypothesis segmentation
        :param window_size: optional
        """
        calculator = self.calculator_dict[calc_type]
        weight = self.weight_dict[calc_type]
        if window_size != -1:
            result_dict = calculator(h_dataset, gold_dataset, window_size=window_size, return_parts=True)
        else:
            result_dict = calculator(h_dataset, gold_dataset, return_parts=True)
        for result in result_dict.values():
            false_seg_count = result[0]
            total_count = result[1]
            if total_count == 0:
                # TODO: Check when happens
                false_prob = -1
            else:
                false_prob = float(false_seg_count) / float(total_count)
            weight.append((false_prob, total_count))

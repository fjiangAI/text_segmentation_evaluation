from segeval.window.pk import pk
from segeval.window.windowdiff import window_diff as WD
from segeval.similarity.boundary import boundary_similarity as B
from segeval.similarity.segmentation import segmentation_similarity as S
from segeval.format import *
from segeval.similarity import boundary_confusion_matrix
from segeval.ml import precision, recall, fmeasure


def example_in_paper_test():
    gold = [2, 3, 6]
    h_list = [[5, 6], [2, 2, 7], [2, 3, 3, 3], [1, 1, 3, 1, 5]]
    for n, h in enumerate(h_list):
        cm = boundary_confusion_matrix(h, gold)
        print("第%d次实验" % int(n + 1))
        # The P, R and F values are different from those in the normal method because it will correct the near missing.
        print("P=%.4f, R=%.4f, F=%.4f" % (precision(cm), recall(cm), fmeasure(cm)))
        print("1-Pk=%.3f, 1-WD=%.3f, B=%.3f, S=%.3f" % (pk(h, gold, one_minus=True),
                                                    WD(h, gold, one_minus=True, window_size=2), B(h, gold), S(h, gold)))


def format_convert_test():
    # mass format [2, 3, 6]
    masses = [2, 3, 6]
    # position format (1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3)
    positions = convert_masses_to_positions(masses)
    # boundary_string ({0},{1},{0},{0},{1},{0},{0},{0},{0},{0},)
    boundary_string = boundary_string_from_masses(masses)
    print(positions)
    print(boundary_string)


if __name__ == '__main__':
    example_in_paper_test()
    format_convert_test()

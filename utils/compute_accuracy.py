


def compute_accuracy(predictions, gold_labels, neutral_lower=-0.33, neural_upper=0.33):
    map_predictions(predictions, neutral_lower, neural_upper)
    spearman_corr = compute_spearman(predictions, gold_labels)

def map_predictions(predictions, neutral_lower, neutral_upper):
    for itr in range(len(predictions)):
        if predictions[itr] <= neutral_lower:
            predictions[itr] = -1
        elif predictions[itr] <= neutral_upper:
            predictions[itr] = 0
        else:
            predictions[itr] = 1

def compute_spearman(predictions, gold_labels):
    observation_length = len(predictions)
    diff_sqr_sum = 0
    for i in range(observation_length):
        diff_sqr_sum += (predictions[i] - gold_labels[i]) ** 2

    spearman_corr = 1 - ((6 * diff_sqr_sum) / (observation_length * (observation_length**2 - 1)))
    return spearman_corr

# testing spearman
# a = [3, 4, 2, 1, 6, 7, 5]
# b = [3, 2, 1, 5, 7, 4, 6]
# print(compute_spearman(a, b))
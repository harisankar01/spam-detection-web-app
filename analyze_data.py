import json
import pandas as pd
from scipy import stats
def read_dataset(file_path):
    with open(file_path, 'r') as file:
        data = [json.loads(line) for line in file]

    return pd.DataFrame(data)

def compute_weighted_mean_rating(reviews, honesty_values):
    total_weighted_sum = 0
    total_weight = 0

    for _, review in reviews.iterrows():
        reviewer_id = review['reviewerID']
        rating = review['overall']


        if reviewer_id in honesty_values:
            honesty = honesty_values[reviewer_id]
            total_weighted_sum += rating * honesty
            total_weight += honesty

    return total_weight / total_weighted_sum if total_weight > 0 else 0

def compute_honesty_and_disagreements(reviews, weighted_mean_rating):
    honesty_values = {}
    disagree_count = 0

    for _, review in reviews.iterrows():
        reviewer_id = review['reviewerID']
        rating = review['overall']
        honesty = 1.0

        if (rating < weighted_mean_rating and weighted_mean_rating >= 3) or (rating >= weighted_mean_rating and weighted_mean_rating < 3):
            disagree_count += 1
            honesty = 1 - (disagree_count / len(reviews))

        honesty_values[reviewer_id] = honesty

    return honesty_values, disagree_count

def compute_spamcity_with_exponential_smoothing(data,rounds, alpha, threshold_difference=0.01):
    spamcity_values = {}
    overall_spamcity = {reviewer_id: 0.0 for reviewer_id in data['reviewerID'].unique()}

    prev_honesty_values = {reviewer_id: 1.0 for reviewer_id in overall_spamcity}

    round_counter = 1

    while round_counter <= rounds:
        for _, reviews in data.groupby('asin'):
            weighted_mean_rating = compute_weighted_mean_rating(reviews, prev_honesty_values)
            honesty_values, disagree_count = compute_honesty_and_disagreements(reviews, weighted_mean_rating)
            phi = disagree_count / len(data)
            for reviewer_id, honesty in honesty_values.items():
                psi = 1 - stats.binom.cdf(disagree_count, len(data), phi)
                s = 1 - psi
                overall_spamcity[reviewer_id] = alpha * s + (1 - alpha) * overall_spamcity[reviewer_id]


        if all(
            reviewer_id in prev_honesty_values and reviewer_id in honesty_values
            and abs(prev_honesty_values[reviewer_id] - honesty_values[reviewer_id]) < threshold_difference
            for reviewer_id in set(prev_honesty_values) | set(honesty_values)
        ):
            break

        prev_honesty_values = honesty_values.copy()
        round_counter += 1

    return overall_spamcity
import numpy as np

def calculate_relevance_scores(correct_answers, predictions):
    return np.array([1 if pred in correct_answers else 0 for pred in predictions])

def dcg(scores):
    """Compute DCG based on the relevance scores."""
    return np.sum((2**scores - 1) / np.log2(np.arange(2, len(scores) + 2)))

def ndcg(correct_answers, predictions):
    relevance_scores = calculate_relevance_scores(correct_answers, predictions)
    ideal_scores = calculate_relevance_scores(correct_answers, correct_answers) # Perfect ranking
    
    dcg_value = dcg(relevance_scores)
    idcg_value = dcg(ideal_scores)
    
    return dcg_value / idcg_value if idcg_value > 0 else 0

# Your example
correct_answers = ['a', 'b', 'c', 'd']
predictions = ['a', 'c', 'f', 'd']

ndcg_value = ndcg(correct_answers, predictions)
print(f"NDCG: {ndcg_value}")
# Для поиска наиболее похожих слов:
from difflib import SequenceMatcher

# Ниже располагаются функции для поиска наиболее похожих межжду собой слов (первый шаг проверки кандидата)
def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def check_similarity(word1, word2, threshold=0.6):
    ratio = similar(word1, word2)
    return ratio>= threshold

def select_most_similar(input_word, filter_words, threshold=0.6):
    best_match = None
    best_similarity = 0
    for filter_word in filter_words:
        similarity = similar(input_word, filter_word)
        if similarity > best_similarity and similarity >= threshold:
            best_similarity = similarity
            best_match = filter_word
    return best_match if best_match is not None else input_word

def process_skills(input_words, filter_words, threshold=0.6):
    processed_skills = []
    for input_word in input_words:
        processed_skill = select_most_similar(input_word, filter_words, threshold)
        processed_skills.append(processed_skill)
    return processed_skills

def filter_list(original_list, filter_list, threshold=0.7):
    filtered_list = []
    for word1 in filter_list:
        add_word = True
        for word2 in original_list:
            if check_similarity(word1, word2, threshold):
                add_word = False
                break
        if add_word:
            filtered_list.append(word1)
    return filtered_list
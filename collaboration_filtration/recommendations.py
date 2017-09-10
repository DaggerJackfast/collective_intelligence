from math import sqrt

critics = {
    "Lisa Rose": {
        "Lady in the Water": 2.5,
        "Snakes on a Plane": 3.5,
        "Just My Luck": 3.0,
        "Superman Returns": 3.5,
        "You, Me and Dupree": 2.5,
        "The Night Listener": 3.0
    },
    "Gene Seymour": {
        "Lady in the Water": 3.0,
        "Snakes on a Plane": 3.5,
        "Just My Luck": 1.5,
        "Superman Returns": 5.0,
        "The Night Listener": 3.0,
        "You, Me and Dupree": 3.5
    },
    "Michael Phillips": {
        "Lady in the Water": 2.5,
        "Snakes on a Plane": 3.0,
        "Superman Returns": 3.5,
        "The Night Listener": 4.0
    },
    "Claudia Puig": {
        "Snakes on a Plane": 3.5,
        "Just My Luck": 3.0,
        "The Night Listener": 4.5,
        "Superman Returns": 4.0,
        "You, Me and Dupree": 2.5
    },
    "Mick LaSalle": {
        "Lady in the Water": 3.0,
        "Snakes on a Plane": 4.0,
        "Just My Luck": 2.0,
        "Superman Returns": 3.0,
        "The Night Listener": 3.0,
        "You, Me and Dupree": 2.0
    },
    "Jack Matthews": {
        "Lady in the Water": 3.0,
        "Snakes on a Plane": 4.0,
        "The Night Listener": 3.0,
        "Superman Returns": 5.0,
        "You, Me and Dupree": 3.5
    },
    "Toby": {
        "Snakes on a Plane": 4.5,
        "You, Me and Dupree": 1.0,
        "Superman Returns": 4.0
    }
}


def transform_prefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            # Обменять местами человека и предмет
            result[item][person] = prefs[person][item]
    return result


# Возвращает оценку подобия first_person и second_person на основе расстояния
def sim_distance(prefs, first_person, second_person):
    # Получить список предметов оцененных обоими
    si = {}
    for item in prefs[first_person]:
        if item in prefs[second_person]:
            si[item] = 1
    # Eсли нет ни общей оценки, вернуть 0
    if len(si) == 0: return 0

    sum_of_squares = sum(pow(prefs[first_person][item] - prefs[second_person][item], 2)
                         for item in prefs[first_person] if item in prefs[second_person])
    return 1 / (1 + sum_of_squares)


# Возвращает коэфицинт корреляции Пирсона между first_person second_person
def sim_pearson(prefs, first_person, second_person):
    # Получить список предметов, оцененных обоими
    si = {}
    for item in prefs[first_person]:
        if item in prefs[second_person]:
            si[item] = 1
    # Найти число элементов
    n = len(si)
    # Если нет ни одной общей оценки, вернуть 0
    if n == 0: return 0
    # Вычислить сумму всех предпочтений
    sum_first = sum([prefs[first_person][item] for item in si])
    sum_second = sum([prefs[second_person][item] for item in si])

    # Вычислить сумму квадратов
    sum_first_square = sum([pow(prefs[first_person][item], 2) for item in si])
    sum_second_square = sum([pow(prefs[second_person][item], 2) for item in si])
    # Вычислить сумму произведений
    sum_product = sum([prefs[first_person][item] * prefs[second_person][item] for item in si])
    # Вычислить коэфициент Пирсона
    num = sum_product - (sum_first * sum_second / n)
    den = sqrt((sum_first_square - pow(sum_first, 2) / n) * (sum_second_square - pow(sum_second, 2) / n))
    if den == 0: return 0
    coefficient = num / den
    return coefficient


# Возвращает список наилучших соответствий для человека из словаря prefs.
# Количество результатов в списке и функция подобия - необязательные параметры
def top_matches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    # Отсортировать список по убыванию оценок
    scores.sort()
    scores.reverse()
    return scores[0:n]


# Получить рекомендации для заданного человека, пользуясь взвешенным средним
# оценок, данных всеми остальными пользователями
def get_recommendations(prefs, person, similarity=sim_pearson):
    totals = {}
    sim_sums = {}
    for other in prefs:
        # сравнивать меня с собой же не нужно
        if other == person: continue
        sim = similarity(prefs, person, other)
        # игнорировать нулевые и отрицательные оценки
        if sim <= 0: continue
        for item in prefs[other]:
            # оценивать только фильмы, которые я еще не смотрел
            if item not in prefs[person] or prefs[person][item] == 0:
                # Коэфициент подобия * оценка
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # Сумма коэффициентов подобия
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim
    rankings = [(total / sim_sums[item], item) for item, total in totals.items()]
    # Вернуть отсотрированный список
    rankings.sort()
    rankings.reverse()
    return rankings

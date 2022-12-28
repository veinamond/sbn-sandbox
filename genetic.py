import functools
import random


def using_1p1(init_vec, fit_function, mutation, iterations):
    cur_vec = init_vec
    cur_fit = fit_function(cur_vec)
    n = len(init_vec)
    for _ in range(iterations):
        new_vec = mutation(cur_vec)
        new_fit = fit_function(new_vec)
        if new_fit <= cur_fit:
            cur_vec = new_vec
            cur_fit = new_fit

    return cur_vec


def using_1cl(init_vec, fit_function, mutation, lmbd, iterations):
    if lmbd < 1:
        raise ValueError('Lambda parameter in (1,lambda) algorithm must be >= 1')

    cur_vec = init_vec
    n = len(init_vec)
    for _ in range(iterations):
        new_opt_vec = None
        new_opt_fit = None
        for _ in range(lmbd):
            new_vec = mutation(cur_vec)
            new_fit = fit_function(new_vec)
            if not new_opt_fit or new_fit < new_opt_fit:
                new_opt_vec = new_vec
                new_opt_fit = new_fit
        cur_vec = new_opt_vec

    return cur_vec


def using_custom_ga(init_vec, fit_function, mutation, crossover, l, h, g, iterations):
    if l < 0 or h < 0 or g < 0 or l + h + g < 1:
        raise ValueError('l, h and g parameters must be non-negative integers; also l + h + g must be >= 1')
    if g % 2 == 1:
        raise ValueError('g must be even number')

    def cmp_by_2nd(i1, i2):
        return 0 if i1[1] == i2[1] else (1 if i1[1] < i2[1] else -1)

    sz = l + h + g      # population size
    population = [init_vec] * sz
    for _ in range(iterations):
        new_population = []
        u = [(i, 1 / fit_function(population[i])) for i in range(sz)]

        u.sort(key=functools.cmp_to_key(cmp_by_2nd))

        [new_population.append(population[u[i][0]]) for i in range(l)]          # elitism

        for _ in range(h):
            i = weighted_random_index(u)
            new_population.append(mutation(population[i]))                      # mutation

        for _ in range(g // 2):
            i1, i2 = weighted_random_index(u), weighted_random_index(u)
            new_population.extend(crossover(population[i1], population[i2]))    # crossover

        population = new_population

    population_with_fit = [(item, fit_function(item)) for item in population]
    return min(population_with_fit, key=functools.cmp_to_key(cmp_by_2nd))[0]


def weighted_random_index(u):
    r = random.uniform(0, sum([item[1] for item in u]))
    for i in range(len(u)):
        if r <= u[i][1]:
            return i
        else:
            r -= u[i][1]
    raise AssertionError('Unreachable state')

def default_mutation(vec):
    n = len(vec)
    return [1 - vec[i] if random.randrange(n) == 0 else vec[i] for i in range(n)]

def two_point_crossover(vec1, vec2):
    n = len(vec1)
    i1, i2 = random.randrange(n), random.randrange(n - 1)
    if i2 >= i1:
        i2 += 1

    new_vec1, new_vec2 = [], []
    for i in range(n):
        if i < i1 == i < i2:
            new_vec1.append(vec1[i])
            new_vec2.append(vec2[i])
        else:
            new_vec1.append(vec2[i])
            new_vec2.append(vec1[i])

    return new_vec1, new_vec2

import functools
import random
from copy import copy


def using_1p1(init_vec, fit_function, mutation, stop_criteria):
    cur_vec = init_vec
    cur_fit = fit_function(cur_vec)
    iterations = 0
    stagnations = 0
    while not ((stop_criteria.is_iteration_count() and iterations >= stop_criteria.get_iteration_count())
               or (stop_criteria.is_stagnation_count() and stagnations >= stop_criteria.get_stagnation_count())):
        new_vec = mutation(cur_vec)
        new_fit = fit_function(new_vec)

        iterations += 1
        if new_fit < cur_fit:
            stagnations = 0
        else:
            stagnations += 1

        if new_fit <= cur_fit:
            cur_vec = new_vec
            cur_fit = new_fit

    return cur_vec, {'iterations': iterations}


def using_1cl(init_vec, fit_function, mutation, lmbd, stop_criteria):
    if lmbd < 1:
        raise ValueError('Lambda parameter in (1,lambda) algorithm must be >= 1')

    cur_vec = copy(init_vec)
    best_vec = copy(init_vec)
    best_fit = None
    iterations = 0
    stagnations = 0
    while not ((stop_criteria.is_iteration_count() and iterations >= stop_criteria.get_iteration_count())
               or (stop_criteria.is_stagnation_count() and stagnations >= stop_criteria.get_stagnation_count())):
        new_opt_vec = None
        new_opt_fit = None
        for _ in range(lmbd):
            new_vec = mutation(cur_vec)
            new_fit = fit_function(new_vec)
            if not new_opt_fit or new_fit < new_opt_fit:
                new_opt_vec = new_vec
                new_opt_fit = new_fit

        iterations += 1
        if best_fit is None or new_opt_fit < best_fit:
            best_vec = new_opt_vec
            best_fit = new_opt_fit
            stagnations = 0
        else:
            stagnations += 1

        cur_vec = new_opt_vec

    return best_vec, {'iterations': iterations}


def using_custom_ga(init_vec, fit_function, mutation, crossover, l, h, g, stop_criteria):
    if l < 0 or h < 0 or g < 0 or l + h + g < 1:
        raise ValueError('l, h and g parameters must be non-negative integers; also l + h + g must be >= 1')
    if g % 2 == 1:
        raise ValueError('g must be even number')

    def cmp_by_2nd_dec(idx1, idx2):
        return 0 if idx1[1] == idx2[1] else (1 if idx1[1] < idx2[1] else -1)

    sz = l + h + g  # population size
    population_with_fit = [with_fit(item, fit_function) for item in [init_vec] * sz]
    iterations = 0
    stagnations = 0
    while not ((stop_criteria.is_iteration_count() and iterations >= stop_criteria.get_iteration_count())
               or (stop_criteria.is_stagnation_count() and stagnations >= stop_criteria.get_stagnation_count())):
        new_population_with_fit = []
        u = [(i, 1 / population_with_fit[i][1]) for i in range(sz)]

        u.sort(key=functools.cmp_to_key(cmp_by_2nd_dec))

        [new_population_with_fit.append(population_with_fit[u[i][0]]) for i in range(l)]  # elitism

        for _ in range(h):
            i = weighted_random_index(u)
            mutated = mutation(population_with_fit[i][0])
            new_population_with_fit.append(with_fit(mutated, fit_function))  # mutation

        for _ in range(g // 2):
            i1, i2 = weighted_random_index(u), weighted_random_index(u)
            crossed_with_fit = [with_fit(crossed, fit_function) for crossed in
                                crossover(population_with_fit[i1][0], population_with_fit[i2][0])]
            new_population_with_fit.extend(crossed_with_fit)  # crossover

        iterations += 1
        best_fit = max(population_with_fit, key=functools.cmp_to_key(cmp_by_2nd_dec))[1]
        new_best_fit = max(new_population_with_fit, key=functools.cmp_to_key(cmp_by_2nd_dec))[1]
        if new_best_fit < best_fit:
            stagnations = 0
        else:
            stagnations += 1

        population_with_fit = new_population_with_fit

    best_in_population = max(population_with_fit, key=functools.cmp_to_key(cmp_by_2nd_dec))[0]
    return best_in_population, {'iterations': iterations}


def weighted_random_index(u):
    r = random.uniform(0, sum([item[1] for item in u]))
    for i in range(len(u)):
        if r <= u[i][1]:
            return i
        else:
            r -= u[i][1]
    raise AssertionError('Unreachable state')


def with_fit(vec, fit_function):
    return vec, fit_function(vec)


def non_increasing_mutation_of(base_mutation, vec, env):
    vec_wt = sum(vec)
    new_vec = None
    new_vec_wt = None
    while new_vec_wt is None or new_vec_wt > vec_wt:
        new_vec = base_mutation(vec, env)
        new_vec_wt = sum(new_vec)
    return new_vec


def default_mutation(vec, env):
    n = len(vec)
    return [1 - vec[i] if random.randrange(n) == 0 else vec[i] for i in range(n)]


def non_increasing_default_mutation(vec):
    return non_increasing_mutation_of(default_mutation, vec, None)


def init_doerr_env(beta, ndiv2):
    env = []
    for i in range(ndiv2):
        env.append((i + 1) ** -beta)
    for i in range(ndiv2 - 1):
        env[i + 1] += env[i]
    last = env[len(env) - 1]
    for i in range(ndiv2):
        env[i] /= last
    return env


def generate_alpha_for_doerr_mutation(env):
    x = random.random()
    for i in range(len(env)):
        if x <= env[i]:
            return i + 1
    raise AssertionError('Unreachable state')


def doerr_mutation(vec, env):
    n = len(vec)
    alpha = generate_alpha_for_doerr_mutation(env)
    return [1 - vec[i] if random.random() < alpha / n else vec[i] for i in range(n)]


def non_increasing_doerr_mutation(vec, env):
    return non_increasing_mutation_of(doerr_mutation, vec, env)


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

import random
from copy import copy


def using_1p1(init_vec, fit_function, iterations, seed=None):
    random.seed(seed)

    cur_vec = copy(init_vec)
    cur_fit = fit_function(cur_vec)
    n = len(init_vec)
    for _ in range(iterations):
        new_vec = [1 - cur_vec[i] if random.randrange(n) == 0 else cur_vec[i] for i in range(n)]
        new_fit = fit_function(new_vec)
        if new_fit <= cur_fit:
            cur_vec = new_vec
            cur_fit = new_fit

    return cur_vec


def using_1cl(init_vec, fit_function, lmbd, iterations, seed=None):
    if lmbd < 1:
        raise ValueError('Lambda parameter in (1,lambda) algorithm must be >= 1')
    random.seed(seed)

    cur_vec = copy(init_vec)
    n = len(init_vec)
    for _ in range(iterations):
        new_opt_vec = None
        new_opt_fit = None
        for _ in range(lmbd):
            new_vec = [1 - cur_vec[i] if random.randrange(n) == 0 else cur_vec[i] for i in range(n)]
            new_fit = fit_function(new_vec)
            if not new_opt_fit or new_fit < new_opt_fit:
                new_opt_vec = new_vec
                new_opt_fit = new_fit
        cur_vec = new_opt_vec

    return cur_vec

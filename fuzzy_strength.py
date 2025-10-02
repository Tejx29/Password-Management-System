import skfuzzy as fuzz
import numpy as np

def password_strength(pw: str) -> str:
    length = len(pw)
    variety = 0
    if any(c.islower() for c in pw):
        variety += 1
    if any(c.isupper() for c in pw):
        variety += 1
    if any(c.isdigit() for c in pw):
        variety += 1
    if any(not c.isalnum() for c in pw):
        variety += 1

    # Universes
    x_len = np.arange(0, 21, 1)
    x_var = np.arange(0, 5, 1)
    x_strength = np.arange(0, 11, 1)

    # Membership functions
    len_low = fuzz.trimf(x_len, [0, 0, 8])
    len_med = fuzz.trimf(x_len, [6, 10, 14])
    len_high = fuzz.trimf(x_len, [12, 20, 20])

    var_low = fuzz.trimf(x_var, [0, 0, 2])
    var_high = fuzz.trimf(x_var, [2, 4, 4])

    strength_low = fuzz.trimf(x_strength, [0, 0, 4])
    strength_med = fuzz.trimf(x_strength, [3, 5, 7])
    strength_high = fuzz.trimf(x_strength, [6, 10, 10])

    # Fuzzify inputs
    len_level_low = fuzz.interp_membership(x_len, len_low, length)
    len_level_med = fuzz.interp_membership(x_len, len_med, length)
    len_level_high = fuzz.interp_membership(x_len, len_high, length)

    var_level_low = fuzz.interp_membership(x_var, var_low, variety)
    var_level_high = fuzz.interp_membership(x_var, var_high, variety)

    # Rules
    active_rule1 = np.fmax(len_level_low, var_level_low)
    strength_activation_low = np.fmin(active_rule1, strength_low)

    active_rule2 = np.fmin(len_level_med, var_level_high)
    strength_activation_med = np.fmin(active_rule2, strength_med)

    active_rule3 = np.fmin(len_level_high, var_level_high)
    strength_activation_high = np.fmin(active_rule3, strength_high)

    # Aggregate
    aggregated = np.fmax(strength_activation_low,
                         np.fmax(strength_activation_med, strength_activation_high))

    if aggregated.sum() == 0:
        return "Weak"

    result = fuzz.defuzz(x_strength, aggregated, 'centroid')

    if result < 4:
        return "Weak"
    elif result < 7:
        return "Medium"
    else:
        return "Strong"

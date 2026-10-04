"""Independent observer-side stationary comparator. Never imported by kernels.

Ideal uniform addressing is assumed; the finite-word modulo bias is neglected.
Stationarity is a prediction to test, not guaranteed by discarding burn-in.
"""

import math


def stationary(charge: int, capacity: int, birth_admission: float) -> list[float]:
    q = abs(charge)
    if capacity < q or capacity < 1 or not 0 <= birth_admission <= 1:
        raise ValueError("Invalid stationary comparator parameters")
    log_weights = [0.0]
    for k in range(1, (capacity-q)//2 + 1):
        death = 2*k*(q+k)/(q+2*k)**2
        log_weights.append(log_weights[-1] + math.log(birth_admission/death) if birth_admission else -math.inf)
    shift = max(log_weights)
    weights = [math.exp(w-shift) for w in log_weights]
    total = sum(weights)
    return [w/total for w in weights]

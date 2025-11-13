import numpy as np

def linear_piecewise_approximation(X, Y, epsilon):
    """
    Uniform ε-approximation of a time series (X, Y)
    Returns:
        alphas: list of slopes (partial trends)
        X_ranges: list of (start_idx, end_idx) tuples
    """

    def find_cone(p0, p2, eps):
        """Compute (γ, β) angles for the cone tangent to ε-circle around p2 from p0."""
        dx = p2[0] - p0[0]
        dy = p2[1] - p0[1]

        if abs(dx) < eps:
            # Avoid division by zero → vertical line
            return -np.pi/2, np.pi/2

        term1 = (dx * dy - eps) / (dx**2 - eps**2)
        term2 = (dx * dy + eps) / (dx**2 - eps**2)

        gamma = np.arctan(term1)
        beta  = np.arctan(term2)
        if gamma > beta:
            gamma, beta = beta, gamma
        return gamma, beta

    alphas = []      # list of slope values (e.g. bisectors)
    X_ranges = []    # list of index ranges
    n = len(X)

    i0 = 0
    while i0 < n - 1:
        p0 = (X[i0], Y[i0])
        i1 = i0 + 1
        p2 = (X[i1], Y[i1])

        # Initial cone
        alpha_min, alpha_max = find_cone(p0, p2, epsilon)

        # Extend cone while intersection not empty
        while i1 < n:
            p2 = (X[i1], Y[i1])
            g2, b2 = find_cone(p0, p2, epsilon)
            new_min, new_max = max(alpha_min, g2), min(alpha_max, b2)

            if new_min <= new_max:  # intersection still valid
                alpha_min, alpha_max = new_min, new_max
                i1 += 1
            else:
                # intersection empty -> segment ends at previous point
                break

        # Compute slope as bisector of the final cone
        slope = np.tan((alpha_min + alpha_max) / 2)
        alphas.append(slope)
        X_ranges.append((i0, i1 - 1))

        i0 = i1 - 1  # start next cone from last valid point

    return alphas, X_ranges

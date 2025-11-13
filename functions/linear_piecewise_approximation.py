import numpy as np

def linear_piecewise_approximation(X, Y, epsilon):
    """
    Uniform ε-approximation of a time series (X, Y)
    following the exact formulas for γ₂ and β₂
    from Kacprzyk, Wilbik, and Zadrożny (2010).
    
    Returns
    -------
    angles_deg : list of float
        Trend angles (degrees) between -90 and 90.
    X_ranges : list of (start_idx, end_idx)
        Index ranges of the piecewise-linear segments.
    """

    def find_cone(p0, p2, eps):
        """Compute (γ, β) according to the paper’s exact equations."""
        dx = p0[0] - p2[0]
        dy = p0[1] - p2[1]

        denom = dx**2 - eps**2
        if denom == 0:
            return -np.pi/2 + 1e-12, np.pi/2 - 1e-12

        inside_sqrt = dx**2 + dy**2 - eps**2
        if inside_sqrt < 0:
            # No valid cone intersection possible (eps too large)
            inside_sqrt = 0.0

        root_term = np.sqrt(inside_sqrt)

        num_gamma = dx * dy - eps * root_term
        num_beta  = dx * dy + eps * root_term

        gamma = np.arctan(num_gamma / denom)
        beta  = np.arctan(num_beta  / denom)

        if gamma > beta:
            gamma, beta = beta, gamma

        # clip to (-90, 90)
        eps_rad = 1e-12
        gamma = np.clip(gamma, -np.pi/2 + eps_rad, np.pi/2 - eps_rad)
        beta  = np.clip(beta,  -np.pi/2 + eps_rad, np.pi/2 - eps_rad)
        return gamma, beta

    angles_deg = []
    X_ranges = []
    n = len(X)
    i0 = 0

    while i0 < n - 1:
        p0 = (X[i0], Y[i0])
        i1 = i0 + 1
        alpha_min, alpha_max = find_cone(p0, (X[i1], Y[i1]), epsilon)

        # extend while intersection non-empty
        while i1 < n:
            g2, b2 = find_cone(p0, (X[i1], Y[i1]), epsilon)
            new_min, new_max = max(alpha_min, g2), min(alpha_max, b2)
            if new_min <= new_max:
                alpha_min, alpha_max = new_min, new_max
                i1 += 1
            else:
                break

        # compute bisector angle in degrees
        angle_rad = 0.5 * (alpha_min + alpha_max)
        angle_deg = np.degrees(angle_rad)
        angle_deg = float(np.clip(angle_deg, -90 + 1e-9, 90 - 1e-9))

        angles_deg.append(angle_deg)
        X_ranges.append((i0, i1 - 1))
        i0 = i1 - 1

    return angles_deg, X_ranges

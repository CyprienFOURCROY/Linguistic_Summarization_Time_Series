import matplotlib.pyplot as plt
import numpy as np

def plot_time_series_with_segments_and_epsilon(X, Y, angles_deg, X_ranges, epsilon):
    """
    Plot the original time series and its piecewise-linear ε-approximation.
    Each circle of radius ε around data points is drawn in the same color 
    for points belonging to the same segment.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(X, Y, label='Original Time Series', color='black', linewidth=1, alpha=0.7)
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(X_ranges)))  # one color per segment

    for color, (angle_deg, (start, end)) in zip(colors, zip(angles_deg, X_ranges)):
        # segment points
        x_segment = X[start:end+1]
        y_segment = Y[start:end+1]

        # slope from angle
        slope = np.tan(np.radians(angle_deg))
        y_fit = Y[start] + slope * (x_segment - x_segment[0])

        # plot segment line
        plt.plot(x_segment, y_fit, color=color, linewidth=2.5, label=f"Segment {start}-{end}")

        # plot ε-circles
        for x, y in zip(x_segment, y_segment):
            circle = plt.Circle((x, y), epsilon, color=color, fill=False, alpha=0.5, linewidth=1.5)
            plt.gca().add_patch(circle)

    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Time Series with ε-Circles and Piecewise Linear Approximation")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()



def plot_time_series_with_segments(X, Y, angles_deg, X_ranges):
    """
    Plot the original time series and its piecewise linear approximation
    (without epsilon circles).
    
    Parameters
    ----------
    X, Y : array-like
        Original time series data.
    angles_deg : list of float
        Angles (in degrees) for each segment.
    X_ranges : list of (start_idx, end_idx)
        Index ranges corresponding to each segment.
    """
    plt.figure(figsize=(12, 6))
    
    # Original time series (thin black line)
    plt.plot(X, Y, color='black', linewidth=1, alpha=0.6, label='Original Time Series')
    
    # Generate colors for each segment
    colors = plt.cm.tab10(np.linspace(0, 1, len(X_ranges)))
    
    # Draw linear approximations
    for color, (angle_deg, (start, end)) in zip(colors, zip(angles_deg, X_ranges)):
        slope = np.tan(np.radians(angle_deg))
        x_segment = X[start:end+1]
        y_fit = Y[start] + slope * (x_segment - X[start])
        plt.plot(x_segment, y_fit, color=color, linewidth=2.5)

    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Piecewise Linear Approximation of Time Series")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.show()

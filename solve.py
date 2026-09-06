import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution


# Load data
data = pd.read_csv("xy_data.csv")

x_data = data["x"].to_numpy()
y_data = data["y"].to_numpy()


# Original parametric curve
def curve(t, theta_deg, M, X):

    theta = np.deg2rad(theta_deg)

    x = (
        t * np.cos(theta)
        - np.exp(M * np.abs(t))
        * np.sin(0.3 * t)
        * np.sin(theta)
        + X
    )

    y = (
        42
        + t * np.sin(theta)
        + np.exp(M * np.abs(t))
        * np.sin(0.3 * t)
        * np.cos(theta)
    )

    return x, y


# Objective function
def objective(params):

    theta_deg, M, X = params

    theta = np.deg2rad(theta_deg)

    # Transform observed points
    u = (
        (x_data - X) * np.cos(theta)
        + (y_data - 42) * np.sin(theta)
    )

    v = (
        -(x_data - X) * np.sin(theta)
        + (y_data - 42) * np.cos(theta)
    )

    # Enforce t range
    if np.any(u < 6) or np.any(u > 60):
        return 1e6

    # Expected v
    v_expected = (
        np.exp(M * u) * np.sin(0.3 * u)
    )

    # L1 error
    return np.mean(np.abs(v - v_expected))


# Parameter bounds
bounds = [
    (0, 50),        # theta
    (-0.05, 0.05),  # M
    (0, 100)        # X
]


# Optimize
result = differential_evolution(
    objective,
    bounds,
    seed=42,
    tol=1e-10,
    polish=True
)


# Results
theta_best = result.x[0]
M_best = result.x[1]
X_best = result.x[2]

print("Optimization finished")
print("---------------------")

print(f"Theta = {theta_best:.12f} degrees")
print(f"M     = {M_best:.12f}")
print(f"X     = {X_best:.12f}")

print(f"L1 error = {result.fun:.12e}")


# Validation
t = np.linspace(6, 60, 1500)

x_pred, y_pred = curve(
    t,
    theta_best,
    M_best,
    X_best
)


plt.figure(figsize=(10, 6))

plt.scatter(
    x_data,
    y_data,
    s=5,
    label="CSV data"
)

plt.plot(
    x_pred,
    y_pred,
    linewidth=2,
    label="Fitted curve"
)

plt.xlabel("x")
plt.ylabel("y")
plt.title("CSV Data vs Fitted Parametric Curve")
plt.legend()
plt.grid(True)

plt.savefig(
    "fitted_curve.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

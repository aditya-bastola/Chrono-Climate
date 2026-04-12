import numpy as np
from sklearn.linear_model import LinearRegression


def calculate_depletion_year(years_list, pixel_counts_list):
    """Fit a linear regression on historical water-pixel data and solve for
    the year the count reaches zero."""

    X = np.array(years_list).reshape(-1, 1)
    y = np.array(pixel_counts_list)

    model = LinearRegression()
    model.fit(X, y)

    slope = model.coef_[0]
    intercept = model.intercept_

    if slope >= 0:
        return "No depletion trend detected — water area is stable or growing."

    depletion_year = int(-intercept / slope)
    return depletion_year

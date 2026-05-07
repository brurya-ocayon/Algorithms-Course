import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer


def main():
    # Load the dataset
    data = load_breast_cancer()
    X = data.data
    y = data.target

    feature_names = data.feature_names

    print("Feature names:", feature_names)
    print("X.shape:", X.shape)
    print("y.shape:", y.shape)

    # Pick two features
    feature_x = 1
    feature_y = 4

    x_vals = X[:, feature_x]
    y_vals = X[:, feature_y]

    # Split by class
    malignant = y == 0
    benign = y == 1

    # --- Exercise: fill in this section ---

    plt.scatter(
        x_vals[malignant],
        y_vals[malignant],
        color='red',
        label='Malignant',
        alpha=0.7
    )

    plt.scatter(
        x_vals[benign],
        y_vals[benign],
        color='blue',
        label='Benign',
        alpha=0.7
    )

    # --- End of exercise section ---

    plt.xlabel(feature_names[feature_x])
    plt.ylabel(feature_names[feature_y])
    plt.title('Wisconsin Cancer Dataset — two features')
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()
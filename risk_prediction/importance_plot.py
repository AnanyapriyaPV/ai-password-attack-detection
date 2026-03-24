import matplotlib.pyplot as plt

def plot_importance(model, feature_names):

    importance = model.feature_importances_

    plt.barh(feature_names, importance)
    plt.title("Feature Importance")
    plt.show()
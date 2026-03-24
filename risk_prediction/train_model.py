import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from risk_prediction.feature_extraction import extract_features


def train_model(X, y):

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100)

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("\nConfusion Matrix:\n")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))

    joblib.dump(model, "trained_model.pkl")

    return model


# THIS PART MAKES THE FILE RUN DIRECTLY
if __name__ == "__main__":

    X, y = extract_features("login_events.csv")

    train_model(X, y)


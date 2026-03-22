import joblib

def load_model():

    model = joblib.load("trained_model.pkl")
    return model


def predict_risk(model, feature_vector):

    prediction = model.predict([feature_vector])[0]

    return prediction
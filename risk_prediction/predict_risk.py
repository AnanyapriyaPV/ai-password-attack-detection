import joblib

def load_model():

    model = joblib.load("risk_prediction/trained_model.pkl")
    return model


def predict_risk(model, feature_vector):

    prediction = model.predict([feature_vector])[0]

    return prediction

def predict_risk_proba(model, feature_vector):
    return model.predict_proba([feature_vector])[0][1]
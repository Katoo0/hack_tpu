import pickle

from preprocessing import Preprocessor

class Predictor:
  def _load_models(self):
    models_name = ['BankA', 'BankB', 'BankC', 'BankD', 'BankE']
    models =[]

    for name in models_name:
       models.append(pickle.load(open(f'models/{name}.sav', 'rb')))
    return models

  def _predict(self, data, models):
    predictions = []
    for i in range(5):
      predictions.append(models[i].predict_proba(data)[:,1])
    return predictions

  def predict_decision(self, values):
    preprocessor = Preprocessor()
    data = preprocessor.preprocessing(values)
    models = self._load_models()
    predictions = self._predict(data, models)
    predictions = [arr.item() for arr in predictions]
    return predictions
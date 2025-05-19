import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score
import joblib


datos = pd.read_csv('datos.csv')
datos['disease'] = (datos.num > 0) * 1

X = datos.drop(columns=['num','disease'])
y = datos.disease

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=99, stratify=y)

modelo = xgb.XGBClassifier(n_estimators=100,learning_rate=0.1,subsample=0.8,colsample_bytree=0.8,random_state=99)
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)

exactitud = accuracy_score(y_test, y_pred)
print(f'Exactitud del modelo: {exactitud:.2f}')

joblib.dump(modelo, 'modelo_xgboost.pkl') # Serializar el modelo

medianas = X.median()
joblib.dump(medianas, 'medianas.pkl') # Serializar las medianas
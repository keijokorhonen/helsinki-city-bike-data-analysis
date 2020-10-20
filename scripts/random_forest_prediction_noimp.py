import numpy as np
import pandas as pd
import pathlib
import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.base import clone 
import eli5
from eli5.sklearn import PermutationImportance
from time import perf_counter

pd.set_option("display.max_rows", None, "display.max_columns", None)

current_folder = pathlib.Path(__file__).parent.absolute()
main_folder = current_folder.parent
data_folder = main_folder / "training_data"
results_folder = main_folder / "results"

X = pd.read_csv(data_folder / "X_train.csv")
y = pd.read_csv(data_folder / "Y_train.csv")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
X_pred = pd.read_csv(data_folder / "X_pred.csv")
pred_pairs = np.loadtxt(data_folder / "train_pairs.txt", dtype=str, delimiter=",")
predictions = pd.DataFrame(columns=y.columns)
predictions_opt = pd.DataFrame(columns=y.columns)

# Writing headers to the predictions dataframe and score records file
score_headers = ["Label","Train Score","OOB Score","Test Score"]
with open(main_folder / 'results' / 'model_prediction_scores.csv', 'a') as outfile:
    newFileWriter = csv.writer(outfile) 
    newFileWriter.writerow(score_headers)

counter = 1
start_time = perf_counter()
model = RandomForestRegressor(n_estimators = 100, max_depth=5, oob_score = True, random_state=42)
for column in y.columns:
    print("Predicting label: " + column)
    model.fit(X_train, y_train[column])    
    # Testing the model trained on all features
    orig_train_score = model.score(X_train, y_train[column])
    orig_oob_score = model.oob_score_
    orig_test_score = model.score(X_test, y_test[column])
    # Using the model to predict the values for the missing pairs of districts and appending them to the results
    prediction = model.predict(X_pred)
    pred_series = pd.Series(prediction)
    predictions[column] = pred_series
    # Writing the test scores for prediction for this label into a file
    csv_line = [column, orig_train_score, orig_oob_score, orig_test_score]
    with open(results_folder / 'model_prediction_scores.csv', 'a') as outfile:
        newFileWriter = csv.writer(outfile) 
        newFileWriter.writerow(csv_line)
    end_time = perf_counter()
    print("Predicted " + str(counter) + " labels in " + str(end_time - start_time) + " s")
    predictions.to_csv(results_folder / "predictions.csv")
    counter += 1
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

def imp_df(column_names, importances):
    data = {
        'Feature': column_names,
        'Importance': importances,
    }
    df = pd.DataFrame(data) \
        .set_index('Feature') \
        .sort_values('Importance', ascending=True)

    return df

# A function for determining the importanceof different features
def drop_col_feat_imp(model, X_train, y_train):
    # clone the model to have the exact same specification as the one initially trained
    model_clone = clone(model)
    # set random_state for comparability
    # random_state = 42
    # model_clone.random_state = random_state
    # training and scoring the benchmark model
    model_clone.fit(X_train, y_train)
    benchmark_score = model_clone.score(X_train, y_train)
    # list for storing feature importances
    importances = []
    # iterating over all columns and storing feature importance (difference between benchmark and new model)
    counter = 1
    for col in X_train.columns:
        # print("Testing column " + str(counter) + " of " + str(len(X_train.columns)))
        model_clone = clone(model)
        #m odel_clone.random_state = random_state
        model_clone.fit(X_train.drop(col, axis = 1), y_train)
        drop_col_score = model_clone.score(X_train.drop(col, axis = 1), y_train)
        importances.append(benchmark_score - drop_col_score)
        counter += 1
    
    importances_df = imp_df(X_train.columns, importances)
    return importances_df

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

# Set the threshold for feature importance; features less important than this will not be use for training the model
threshold = 0.0

# Writing headers to the predictions dataframe and score records file
score_headers = ["Label","Orig. Train Score","Orig. OOB Score","Orig. Test Score","Features Used","Opt. Train Score","Opt. OOB Score","Opt. Test Score"]
with open(main_folder / 'results' / 'model_prediction_scores.csv', 'a') as outfile:
    newFileWriter = csv.writer(outfile) 
    newFileWriter.writerow(score_headers)

counter = 1
start_time = perf_counter()
for column in y.columns:
    print("Predicting label: " + column)
    model = RandomForestRegressor(n_estimators = 100, max_depth=5, oob_score = True, random_state=42)
    model.fit(X_train, y_train[column])    
    # Testing the model trained on all features
    orig_train_score = model.score(X_train, y_train[column])
    orig_oob_score = model.oob_score_
    orig_test_score = model.score(X_test, y_test[column])
    # Using the un-optimised model to predict the values for the missing pairs of districts and appending them to the results
    prediction = model.predict(X_pred)
    pred_series = pd.Series(prediction)
    predictions[column] = pred_series
    # Calculating the importances of the features using the drop column method    
    importances_df = drop_col_feat_imp(model, X_train, y_train[column])
    # Pruning out all features that are less important than the threshold
    pruned_X_train = X_train.copy()
    pruned_X_test = X_test.copy()
    pruned_X_pred = X_pred.copy()
    for index, row in importances_df.iterrows():
        if (row['Importance'] < threshold) & (len(pruned_X_train.columns) > 25):
            pruned_X_train = pruned_X_train.drop([index], axis=1)
            pruned_X_test = pruned_X_test.drop([index], axis=1)
            pruned_X_pred = pruned_X_pred.drop([index], axis=1)
    # Training the model on the pruned features and testing it
    model.fit(pruned_X_train, y_train[column])
    opt_train_score = model.score(pruned_X_train, y_train[column])
    opt_oob_score = model.oob_score_
    opt_test_score = model.score(pruned_X_test, y_test[column])
    # Using the optimised model to predict the values for the missing pairs of districts and appending them to the results
    prediction_opt = model.predict(pruned_X_pred)
    pred_series_opt = pd.Series(prediction_opt)
    predictions_opt[column] = pred_series_opt
    # Saving the feature importances for the label to a file
    filename = "importances_" + column + ".csv"
    importances_df = importances_df.sort_values('Importance', ascending=False)
    importances_df.to_csv(results_folder / filename)
    # Writing the test scores for prediction for this label into a file
    csv_line = [column, orig_train_score, orig_oob_score, orig_test_score, len(pruned_X_train.columns), opt_train_score, opt_oob_score, opt_test_score]
    with open(results_folder / 'model_prediction_scores.csv', 'a') as outfile:
        newFileWriter = csv.writer(outfile) 
        newFileWriter.writerow(csv_line)
    end_time = perf_counter()
    print("Predicted " + str(counter) + " labels in " + str(end_time - start_time) + " s")
    predictions.to_csv(results_folder / "predictions.csv")
    predictions_opt.to_csv(results_folder / "predictions_opt.csv")
    counter += 1
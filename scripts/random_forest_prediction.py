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
        .sort_values('Importance', ascending=False)

    return df

# A function for determining the importanceof different features
def drop_col_feat_imp(model, X_train, y_train, random_state = 42):
    # clone the model to have the exact same specification as the one initially trained
    model_clone = clone(model)
    # set random_state for comparability
    model_clone.random_state = random_state
    # training and scoring the benchmark model
    model_clone.fit(X_train, y_train)
    benchmark_score = model_clone.score(X_train, y_train)
    # list for storing feature importances
    importances = []
    # iterating over all columns and storing feature importance (difference between benchmark and new model)
    counter = 1
    for col in X_train.columns:
        print("Testing column " + str(counter) + " of " + str(len(X_train.columns)))
        model_clone = clone(model)
        model_clone.random_state = random_state
        model_clone.fit(X_train.drop(col, axis = 1), y_train)
        drop_col_score = model_clone.score(X_train.drop(col, axis = 1), y_train)
        importances.append(benchmark_score - drop_col_score)
        counter += 1
    
    importances_df = imp_df(X_train.columns, importances)
    return importances_df


current_folder = pathlib.Path(__file__).parent.absolute()
main_folder = current_folder.parent
data_folder = main_folder / "training_data"

X = pd.read_csv(data_folder / "X_train.csv")
y = pd.read_csv(data_folder / "Y_train.csv")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Scaling the features since they vary quite a lot in range
# sc = StandardScaler()
# X_train = sc.fit_transform(X_train)
# X_test = sc.transform(X_test)

model = RandomForestRegressor(n_estimators = 100,
                           n_jobs = -1,
                           oob_score = True,
                           bootstrap = True)

model.fit(X_train, y_train["base_to_comp_mon_day"])

# Scoring the model on the training and test data (coefficient of determination, R^2)
# if too high, the model is overfitting
train_score = model.score(X_train, y_train["base_to_comp_mon_day"])
print("Training score: " + str(train_score))
oob_score = model.oob_score_
print("OOB Score: " + str(oob_score))
test_score = model.score(X_test, y_test["base_to_comp_mon_day"])
print("Test score: " + str(test_score))
cross_val_scores = cross_val_score(model, X_train, y_train, cv=5)
print(model.feature_importances_)

# Calculating the feature importances using the Drop Column method
# start_time = perf_counter()
# importances_df = drop_col_feat_imp(model, X_train, y_train["base_to_comp_mon_day"], random_state = 42)
# end_time = perf_counter()
# print(importances_df)
# print("Time taken: " + str(end_time - start_time) + " s")

# Calculating the feature importances using the Permutation Feature method
# start_time = perf_counter()
# perm = PermutationImportance(model, cv = None, refit = False, n_iter = 10).fit(X_train, y_train["base_to_comp_mon_day"])
# perm_imp_eli5 = imp_df(X_train.columns, perm.feature_importances_)
# end_time = perf_counter()
# print(perm_imp_eli5)
# print("Time taken: " + str(end_time - start_time) + " s")

X_pred = pd.read_csv(data_folder / "X_pred.csv")
# pred_pairs = np.loadtxt(data_folder / "train_pairs.txt", dtype=str, delimiter=",")

predictions = model.predict(X_pred)
print(predictions)


# Set the threshold for feature importance; features less important than this will not be use for training the model
threshold = 0.001
predictions = []
# Writing headers to the score records file
score_headers = '"Label","Orig. Train Score","Orig. OOB Score","Orig. Test Score","Features Used","Opt. Train Score","Opt. OOB Score","Opt. Test Score"'
    with open(main_folder / 'results' / 'model_prediction_scores.csv', 'a') as outfile:
      newFileWriter = csv.writer(outfile) 
      newFileWriter.writerow(score_headers)

counter = 1
start_time = perf_counter
# for column in y.columns:
for column in ["base_to_comp_sun_morning","base_to_comp_sun_day","base_to_comp_sun_evening","base_to_comp_sun_night"]
    print("Predicting label: " + column)
    model = RandomForestRegressor(n_estimators = 100,
                           n_jobs = -1,
                           oob_score = True,
                           bootstrap = True)
    
    model.fit(X_train, y_train[column])    
    # Testing the model trained on all features
    orig_train_score = model.score(X_train, y_train[column])
    orig_oob_score = model.oob_score_
    orig_test_score = model.score(X_test, y_test[column])
    # Calculating the importances of the features using the drop column method    
    importances_df = drop_col_feat_imp(model, X_train, y_train[column], random_state = 42)
    # Pruning out all features that are less important than the threshold
    pruned_X_train = X_train.copy()
    pruned_X_test = X_test.copy()
    pruned_X_pred = X_pred.copy()
    for row in importances_df.iterrows:
      if row['Importance'] < threshold:
        pruned_X_train.drop([row['Feature']], axis=1)
        pruned_X_test.drop([row['Feature']], axis=1)
        pruned_X_pred.drop([row['Feature']], axis=1)
    # Training the model on the pruned features and testing it
    model.fit(pruned_X_train, y_train[column])
    opt_train_score = model.score(pruned_X_train, y_train[column])
    opt_oob_score = model.oob_score_
    opt_test_score = model.score(pruned_X_test, y_test[column])
    # Using the optimised model to predict the values for the missing pairs of districts and appending them to the results
    prediction = model.predict(pruned_X_pred)
    predictions.append(prediction)
    # Saving the feature importances for the label to a file
    filename = "importances_" + column + ".csv"
    importances_df.to_csv(main_folder / "results" / filename)
    # Writing the test scores for prediction for this label into a file
    csv_string = column + "," + str(orig_train_score) + "," + str(orig_oob_score) + "," + str(orig_test_score) + "," + str(len(pruned_X_train.columns)) + "," + str(opt_train_score) + "," + str(opt_oob_score) + "," + str(opt_test_score)
    with open(main_folder / 'results' / 'model_prediction_scores.csv', 'a') as outfile:
      newFileWriter = csv.writer(outfile) 
      newFileWriter.writerow(csv_string)
    end_time = perf_counter()
    print("Predicted " + str(counter) + " labels in " + str(end_time - start_time) + " s")

results = pd.DataFrame(predictions, columns=y.columns)
results.to_csv(main_folder / "results" / "predictions.csv")
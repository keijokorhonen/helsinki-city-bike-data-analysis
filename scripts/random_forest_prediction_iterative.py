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
predictions = pd.DataFrame(columns=y.columns)

# Writing headers to the predictions dataframe and score records file
score_headers = ["Label","Train Score","OOB Score","Test Score"]
with open(main_folder / 'results' / 'model_prediction_scores_iter0.csv', 'a') as outfile:
    newFileWriter = csv.writer(outfile) 
    newFileWriter.writerow(score_headers)

# Predicting the initial ride counts for the new areas
counter = 1
start_time = perf_counter()
model = RandomForestRegressor(n_estimators = 100, max_depth=5, oob_score = True, random_state=42)
for column in y.columns:
    print("Predicting label: " + column)
    model.fit(X_train, y_train[column])
    # Testing the model
    orig_train_score = model.score(X_train, y_train[column])
    orig_oob_score = model.oob_score_
    orig_test_score = model.score(X_test, y_test[column])
    # Using the model to predict the values for the missing pairs of districts and appending them to the results
    prediction = model.predict(X_pred)
    pred_series = pd.Series(prediction)
    predictions[column] = pred_series
    # Writing the test scores for prediction for this label into a file
    csv_line = [column, orig_train_score, orig_oob_score, orig_test_score]
    with open(results_folder / 'model_prediction_scores_iter0.csv', 'a') as outfile:
        newFileWriter = csv.writer(outfile) 
        newFileWriter.writerow(csv_line)
    end_time = perf_counter()
    print("Predicted " + str(counter) + " labels in " + str(end_time - start_time) + " s")
    predictions.to_csv(results_folder / "predictions_iter0.csv")
    counter += 1

# Iterating the process 10 times
iter = 0
while iter < 1:
  # Reading back the predicted ride counts and calculating the predicted total rides in and out for the new areas for the next iteration
  initial_filename = "predictions_iter" + str(iter) + ".csv"
  initial_predictions = pd.read_csv(results_folder / initial_filename).drop(columns=["Unnamed: 0"])
  pair_headers = ['base','comp']
  pred_pairs = pd.read_csv(data_folder / "pred_pairs.txt", names=pair_headers)
  initial_predictions['base'] = pred_pairs['base']
  initial_predictions['comp'] = pred_pairs['comp']
  new_districts = initial_predictions['base'].unique()
  new_district_rides = pd.DataFrame(columns=['comp_to_base_sun_morning','comp_to_base_sun_day','comp_to_base_sun_evening','comp_to_base_sun_night','comp_to_base_mon_morning','comp_to_base_mon_day','comp_to_base_mon_evening','comp_to_base_mon_night','comp_to_base_tue_morning','comp_to_base_tue_day','comp_to_base_tue_evening','comp_to_base_tue_night','comp_to_base_wed_morning','comp_to_base_wed_day','comp_to_base_wed_evening','comp_to_base_wed_night','comp_to_base_thu_morning','comp_to_base_thu_day','comp_to_base_thu_evening','comp_to_base_thu_night','comp_to_base_fri_morning','comp_to_base_fri_day','comp_to_base_fri_evening','comp_to_base_fri_night','comp_to_base_sat_morning','comp_to_base_sat_day','comp_to_base_sat_evening','comp_to_base_sat_night','base_to_comp_sun_morning','base_to_comp_sun_day','base_to_comp_sun_evening','base_to_comp_sun_night','base_to_comp_mon_morning','base_to_comp_mon_day','base_to_comp_mon_evening','base_to_comp_mon_night','base_to_comp_tue_morning','base_to_comp_tue_day','base_to_comp_tue_evening','base_to_comp_tue_night','base_to_comp_wed_morning','base_to_comp_wed_day','base_to_comp_wed_evening','base_to_comp_wed_night','base_to_comp_thu_morning','base_to_comp_thu_day','base_to_comp_thu_evening','base_to_comp_thu_night','base_to_comp_fri_morning','base_to_comp_fri_day','base_to_comp_fri_evening','base_to_comp_fri_night','base_to_comp_sat_morning','base_to_comp_sat_day','base_to_comp_sat_evening','base_to_comp_sat_night'])
  for district in new_districts:
    district_rows = initial_predictions.loc[initial_predictions['base'] == district]
    district_rows = district_rows.drop(columns=['base','comp'])
    district_sums = district_rows.sum(axis = 0)
    district_out_sums = district_sums[0:28]
    district_in_sums = district_sums[28:56]
    district_rides = district_in_sums.append(district_out_sums)
    new_district_rides = new_district_rides.append(district_rides, ignore_index=True)
  new_district_rides.columns = ['comp_rides_in_sun_morning','comp_rides_in_sun_day','comp_rides_in_sun_evening','comp_rides_in_sun_night','comp_rides_in_mon_morning','comp_rides_in_mon_day','comp_rides_in_mon_evening','comp_rides_in_mon_night','comp_rides_in_tue_morning','comp_rides_in_tue_day','comp_rides_in_tue_evening','comp_rides_in_tue_night','comp_rides_in_wed_morning','comp_rides_in_wed_day','comp_rides_in_wed_evening','comp_rides_in_wed_night','comp_rides_in_thu_morning','comp_rides_in_thu_day','comp_rides_in_thu_evening','comp_rides_in_thu_night','comp_rides_in_fri_morning','comp_rides_in_fri_day','comp_rides_in_fri_evening','comp_rides_in_fri_night','comp_rides_in_sat_morning','comp_rides_in_sat_day','comp_rides_in_sat_evening','comp_rides_in_sat_night','comp_rides_out_sun_morning','comp_rides_out_sun_day','comp_rides_out_sun_evening','comp_rides_out_sun_night','comp_rides_out_mon_morning','comp_rides_out_mon_day','comp_rides_out_mon_evening','comp_rides_out_mon_night','comp_rides_out_tue_morning','comp_rides_out_tue_day','comp_rides_out_tue_evening','comp_rides_out_tue_night','comp_rides_out_wed_morning','comp_rides_out_wed_day','comp_rides_out_wed_evening','comp_rides_out_wed_night','comp_rides_out_thu_morning','comp_rides_out_thu_day','comp_rides_out_thu_evening','comp_rides_out_thu_night','comp_rides_out_fri_morning','comp_rides_out_fri_day','comp_rides_out_fri_evening','comp_rides_out_fri_night','comp_rides_out_sat_morning','comp_rides_out_sat_day','comp_rides_out_sat_evening','comp_rides_out_sat_night']
  new_district_rides['district'] = new_districts
  # Reading the original trip data and adding the new trips between the new districts
  original_X_pred = pd.read_csv(data_folder / 'X_pred.csv')
  new_X_pred_demographic = pd.read_csv(data_folder / 'X_pred_somenew.csv')
  new_X_pred_rides = pd.DataFrame(columns=['comp_rides_in_sun_morning','comp_rides_in_sun_day','comp_rides_in_sun_evening','comp_rides_in_sun_night','comp_rides_in_mon_morning','comp_rides_in_mon_day','comp_rides_in_mon_evening','comp_rides_in_mon_night','comp_rides_in_tue_morning','comp_rides_in_tue_day','comp_rides_in_tue_evening','comp_rides_in_tue_night','comp_rides_in_wed_morning','comp_rides_in_wed_day','comp_rides_in_wed_evening','comp_rides_in_wed_night','comp_rides_in_thu_morning','comp_rides_in_thu_day','comp_rides_in_thu_evening','comp_rides_in_thu_night','comp_rides_in_fri_morning','comp_rides_in_fri_day','comp_rides_in_fri_evening','comp_rides_in_fri_night','comp_rides_in_sat_morning','comp_rides_in_sat_day','comp_rides_in_sat_evening','comp_rides_in_sat_night','comp_rides_out_sun_morning','comp_rides_out_sun_day','comp_rides_out_sun_evening','comp_rides_out_sun_night','comp_rides_out_mon_morning','comp_rides_out_mon_day','comp_rides_out_mon_evening','comp_rides_out_mon_night','comp_rides_out_tue_morning','comp_rides_out_tue_day','comp_rides_out_tue_evening','comp_rides_out_tue_night','comp_rides_out_wed_morning','comp_rides_out_wed_day','comp_rides_out_wed_evening','comp_rides_out_wed_night','comp_rides_out_thu_morning','comp_rides_out_thu_day','comp_rides_out_thu_evening','comp_rides_out_thu_night','comp_rides_out_fri_morning','comp_rides_out_fri_day','comp_rides_out_fri_evening','comp_rides_out_fri_night','comp_rides_out_sat_morning','comp_rides_out_sat_day','comp_rides_out_sat_evening','comp_rides_out_sat_night'])
  for index, row in new_X_pred_demographic.iterrows():
    ride_data = new_district_rides.loc[new_district_rides['district'] == row['comp']].squeeze()
    ride_data = ride_data.drop(labels='district')
    new_X_pred_rides = new_X_pred_rides.append(ride_data, ignore_index=True)
  for column in new_X_pred_rides.columns:
    new_X_pred_demographic[column] = new_X_pred_rides[column]
  new_X_pred = new_X_pred_demographic.drop(columns=['base','comp'])
  X_pred = original_X_pred.append(new_X_pred)
  # Copy-pasted the prediction process from above 
  predictions = pd.DataFrame(columns=y.columns)
  # Writing headers to the predictions dataframe and score records file
  score_headers = ["Label","Train Score","OOB Score","Test Score"]
  score_filename = 'model_prediction_scores_iter' + str(iter+1) + '.csv'
  with open(main_folder / 'results' / score_filename, 'a') as outfile:
    newFileWriter = csv.writer(outfile) 
    newFileWriter.writerow(score_headers)
  # Predicting the new ride counts for the new areas
  counter = 1
  start_time = perf_counter()
  model = RandomForestRegressor(n_estimators = 100, max_depth=5, oob_score = True, random_state=42)
  for column in y.columns:
    print("Predicting label: " + column)
    model.fit(X_train, y_train[column])  
    # Testing the model
    orig_train_score = model.score(X_train, y_train[column])
    orig_oob_score = model.oob_score_
    orig_test_score = model.score(X_test, y_test[column])
    # Using the model to predict the values for the missing pairs of districts and appending them to the results
    prediction = model.predict(X_pred)
    pred_series = pd.Series(prediction)
    predictions[column] = pred_series
    # Writing the test scores for prediction for this label into a file
    csv_line = [column, orig_train_score, orig_oob_score, orig_test_score]
    
    with open(results_folder / score_filename, 'a') as outfile:
        newFileWriter = csv.writer(outfile) 
        newFileWriter.writerow(csv_line)
    end_time = perf_counter()
    print("Predicted " + str(counter) + " labels in " + str(end_time - start_time) + " s")
    prediction_filename = "predictions_iter" + str(iter+1) + ".csv"
    predictions.to_csv(results_folder / prediction_filename)
    counter += 1
  iter += 1
  print("Iteration " + str(iter) + " finished.")
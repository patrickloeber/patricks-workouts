"""
Helper file to extract the Export.zip Apple Health data
and dump it into workouts.pickle.

Run this file separately before starting the app.
"""
import zipfile
import shutil
import os
import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path

def _get_heartrate_for_date(start, end, heartrate):
    heartrate = heartrate[heartrate["startDate"] >= start]
    heartrate = heartrate[heartrate["endDate"] <= end]
    return heartrate


def _get_heartrate_for_workout(workout, heartrate):
    if hasattr(workout["startDate"], "item"):
        return _get_heartrate_for_date(workout["startDate"].item(), workout["endDate"].item(), heartrate)
    return _get_heartrate_for_date(workout["startDate"], workout["endDate"], heartrate)


def create_and_save_optimized_file(output_file, xml_file):
    # create element tree object
    tree = ET.parse(xml_file) 
    # for every health record, extract the attributes into a dictionary (columns). Then create a list (rows)
    root = tree.getroot()
    record_list = [x.attrib for x in root.iter('Record')]

    # create DataFrame from a list (rows) of dictionaries (columns)
    record_data = pd.DataFrame(record_list)

    # proper type to dates
    for col in ['creationDate', 'startDate', 'endDate']:
        record_data[col] = pd.to_datetime(record_data[col])

    # value is numeric, NaN if fails
    record_data['value'] = pd.to_numeric(record_data['value'], errors='coerce')

    # some records do not measure anything, just count occurences
    # filling with 1.0 (= one time) makes it easier to aggregate
    record_data['value'] = record_data['value'].fillna(1.0)

    # shorter observation names: use vectorized replace function
    record_data['type'] = record_data['type'].str.replace('HKQuantityTypeIdentifier', '')
    record_data['type'] = record_data['type'].str.replace('HKCategoryTypeIdentifier', '')

    workout_list = [x.attrib for x in root.iter('Workout')]

    # create DataFrame from a list (rows) of dictionaries (columns)
    workout_data = pd.DataFrame(workout_list)
    workout_data['workoutActivityType'] = workout_data['workoutActivityType'].str.replace('HKWorkoutActivityType', '')
    workout_data = workout_data.rename({"workoutActivityType": "Type"}, axis=1)
    # proper type to dates
    for col in ['creationDate', 'startDate', 'endDate']:
        workout_data[col] = pd.to_datetime(workout_data[col])
        
    workout_data['duration'] = pd.to_numeric(workout_data['duration'])
    workout_data['totalEnergyBurned'] = pd.to_numeric(workout_data['totalEnergyBurned'])
    workout_data['totalDistance'] = pd.to_numeric(workout_data['totalDistance'])

    workout_data = workout_data.drop(columns=["device", "sourceVersion"])
    
    heartrate = record_data[record_data["type"] == "HeartRate"]
    
    workout_data["heartrate"] = workout_data.apply(lambda row: _get_heartrate_for_workout(row, heartrate), axis=1)
    workout_data["hr_mean"] = workout_data.apply(lambda row: row['heartrate']["value"].mean(), axis=1)
    
    workout_data.to_pickle(output_file)
    return workout_data


if __name__ == "__main__":
    print('Do workout preprocessing...')

    path = Path("./workouts.pickle")

    if path.is_file():
        path.unlink()

    with zipfile.ZipFile("./Export.zip", "a") as zip:
        zip.extractall("temp") # extract data into current working directory
        
    create_and_save_optimized_file("./workouts.pickle", "./temp/apple_health_export/Export.xml")

    shutil.rmtree("temp")

    os.remove("./Export.zip")

    

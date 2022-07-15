import pandas as pd
import datetime as dt


# This file must exist!
filename="workouts.pickle"
workouts_df = pd.read_pickle(filename)

def get_workouts():
    return workouts_df

def get_last_workout():
    return workouts_df.iloc[[-1]]
    
def get_workout_types():
    return workouts_df.Type.unique()

def split_workouts(workouts):
    strength = workouts[workouts["Type"] == "TraditionalStrengthTraining"]
    functional = workouts[workouts["Type"] == "FunctionalStrengthTraining"]
    hiit = workouts[workouts["Type"] == "HighIntensityIntervalTraining"]
    cross = workouts[workouts["Type"] == "CrossTraining"]
    core = workouts[workouts["Type"] == "CoreTraining"]

    running = workouts[workouts["Type"] == "Running"]
    walking = workouts[workouts["Type"] == "Walking"]

    yoga = workouts[workouts["Type"] == "Yoga"]
    pilates = workouts[workouts["Type"] == "Pilates"]
    flexibility = workouts[workouts["Type"] == "Flexibility"]
    other = workouts[workouts["Type"] == "Other"]
    
    return {'strength': strength, 'functional': functional, 'hiit': hiit,
            'cross': cross, 'core': core, 'running': running, 'walking': walking,
            'yoga': yoga, 'pilates': pilates, 'flexibility': flexibility, 'other': other}
    
    
def get_workouts_month():
    first_of_month = dt.date.today().replace(day=1)
    time_to_check = pd.to_datetime(first_of_month, utc=True)
    return workouts_df[workouts_df["creationDate"] >= time_to_check]

def get_workouts_year():
    first_of_year = dt.date.today().replace(day=1).replace(month=1)
    time_to_check = pd.to_datetime(first_of_year, utc=True)
    return workouts_df[workouts_df["creationDate"] >= time_to_check]

def get_workouts_week():
    today = dt.date.today()
    first_of_week = today - dt.timedelta(days=today.weekday())
    time_to_check = pd.to_datetime(first_of_week, utc=True)
    return workouts_df[workouts_df["creationDate"] >= time_to_check]

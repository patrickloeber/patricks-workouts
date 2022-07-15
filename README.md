# Patrick's Workouts

Displays my Apple Health data in a Steamlit App.

## Instructions

- Export the Apple Health Data from the iPhone. On iPhone go to Health App -> Profile -> Export data -> Send to your computer.
- Put `Export.zip` into this folder and run `python workout_preprocessor.py`. This will output an optimized file `workouts.pickle`
- Run the app: `streamlit run main.py`

## TODO

Find a good way to sync the Health data with this repo.
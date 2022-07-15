import streamlit as st
import workout_service
import matplotlib.pyplot as plt
import datetime as dt

st.title("Patrick's Workouts 🏋🤸🏃‍♂️")

st.markdown(" My workouts. Tracked with my Apple Watch⌚ and analyzed with Python 💛")

st.markdown("Follow me: [Twitter](https://twitter.com/python_engineer) | [YouTube](https://www.youtube.com/c/PythonEngineer)")

st.markdown("Build a Fitness App with Python that sends daily workouts: [Tutorial](https://patloeber.com/fitness-app-harperdb)")

def display_last_workout():
    last_workout = workout_service.get_last_workout()

    st.markdown("## Last Workout👟")
    
    date = last_workout.startDate.item()
    dur = last_workout.duration.item()
    durUnit = last_workout.durationUnit.item()
    totalEnergyBurned = last_workout.totalEnergyBurned.item()
    
    st.markdown(f"**{last_workout.Type.item()}**, {date.strftime('%Y-%m-%d %H:%M')}")
    st.markdown(f"**{dur:.1f} {durUnit}, {int(totalEnergyBurned)} kcal**")
    
    ax = last_workout["heartrate"].iloc[0].plot(x='endDate', y='value', style='r|', markersize=8.5,  figsize=(12, 6), legend=None)
    ax.set_xlabel('Time')
    ax.set_ylabel('HR')
    
    hr_mean = last_workout["heartrate"].iloc[0]["value"].mean()
    
    st.markdown(f"**Heartrate :heart:, {hr_mean:.2f} bpm on average**")
    st.pyplot(ax.figure)
    
def display_workout_summary(wos):    
    for idx in reversed(wos.index):
        workout = wos.loc[idx]
        date = workout.startDate
        dur = workout.duration
        durUnit = workout.durationUnit
        totalEnergyBurned = workout.totalEnergyBurned
        st.markdown(f"{workout.Type}, {date.strftime('%Y-%m-%d %H:%M')}, {dur:.1f} {durUnit}, {int(totalEnergyBurned)} kcal")
      
def display_workout_summary_week():
    wos = workout_service.get_workouts_week()
    st.markdown("## This Week💪")
    
    kcals = wos['totalEnergyBurned'].sum()
    mins = wos['duration'].sum()
    
    n = len(wos)
    st.markdown(f"**{n} Workouts, {int(mins)} minutes, {int(kcals)} kcals**")
    
    today = dt.date.today()

    first_of_week = today - dt.timedelta(days=today.weekday())
    weekdays = [first_of_week]
    for i in range(1, 7):
        weekdays.append(first_of_week + dt.timedelta(days=i))
    weekworkouts = [0] * 7
    for _, row in wos.iterrows():
        d = row["creationDate"].to_pydatetime().date()
        try:
            idx = weekdays.index(d)
            weekworkouts[idx] = int(round(row["duration"]))
        except ValueError:
            pass
        
    wdays = ["Mo", "Tue", "Wed", "Thu", "Fr", "Sat", "Sun"]

    fig = plt.figure(figsize=(12, 6))
    plt.bar(wdays, weekworkouts, color='blue', label="Y1")
    plt.xlabel("Week")
    plt.ylabel("Duration")
    st.pyplot(fig)
    
    
    display_workout_summary(wos)
    
def display_workout_summary_month():
    wos = workout_service.get_workouts_month()
    st.markdown("## This Month💪💪")
    
    kcals = wos['totalEnergyBurned'].sum()
    mins = wos['duration'].sum()
    
    n = len(wos)
    st.markdown(f"**{n} Workouts, {int(mins)} minutes, {int(kcals)} kcals**")
    display_workout_summary(wos)
    
def display_workout_summary_year():
    wos = workout_service.get_workouts_year()
    st.markdown("## This Year🚀")
    
    kcals = wos['totalEnergyBurned'].sum()
    mins = wos['duration'].sum()
    
    n = len(wos)
    st.markdown(f"**{n} Workouts, {int(mins)} minutes, {int(kcals)} kcals**")
    
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = list(wos.Type.value_counts().index)
    sizes = list(wos.Type.value_counts())
    #explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{v:d}'.format(v=val)
        return my_autopct
    

    fig = plt.figure(figsize=(12, 12))
    with plt.style.context({"axes.prop_cycle" : plt.cycler("color", plt.cm.tab20.colors)}):
        ax = fig.add_subplot(121, aspect="equal")
        ax.pie(sizes, labels=labels, autopct=make_autopct(sizes), labeldistance=1.2,
               shadow=True, startangle=0, wedgeprops={'edgecolor': 'black'})
    
    fig1, ax1 = plt.subplots(figsize=(12, 12))
    ax1.pie(sizes, labels=labels, autopct=make_autopct(sizes), labeldistance=1.1,
            shadow=True, startangle=90, wedgeprops={'edgecolor': 'black'})
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig)
    
    display_workout_summary(wos)

display_last_workout()    
display_workout_summary_week()
#display_workout_summary_month()
display_workout_summary_year()
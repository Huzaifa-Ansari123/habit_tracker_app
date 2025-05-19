import streamlit as st
from datetime import date

class Habit:
    def __init__(self, name):
        self.name = name
        self.done_days = set()

    def mark_done(self, day):
        self.done_days.add(day)

    def unmark_done(self, day):
        if day in self.done_days:
            self.done_days.remove(day)

    def is_done(self, day):
        return day in self.done_days

    def count_done(self):
        return len(self.done_days)

class HabitTracker:
    def __init__(self):
        self.habits = {}

    def add(self, name):
        if name and name not in self.habits:
            self.habits[name] = Habit(name)

    def remove(self, name):
        if name in self.habits:
            del self.habits[name]

    def get_all(self):
        return list(self.habits.values())

    def get(self, name):
        return self.habits.get(name)

def main():
    st.title("Habit Tracker")

    if 'tracker' not in st.session_state:
        st.session_state.tracker = HabitTracker()
    tracker = st.session_state.tracker

    st.sidebar.header("Add Habit")
    new_habit = st.sidebar.text_input("Habit name")
    if st.sidebar.button("Add"):
        if new_habit.strip() != "":
            tracker.add(new_habit.strip())
            st.sidebar.success("Added habit")
        else:
            st.sidebar.error("Enter habit name")

    st.sidebar.header("Remove Habit")
    if tracker.get_all():
        to_remove = st.sidebar.selectbox("Choose habit to remove", [h.name for h in tracker.get_all()])
        if st.sidebar.button("Remove"):
            tracker.remove(to_remove)
            st.sidebar.success("Removed habit")
    else:
        st.sidebar.write("No habits here")

    today = date.today()

    st.header("Today's Habits")
    habits = tracker.get_all()
    if not habits:
        st.write("No habits to track. Add some from sidebar.")
        return

    for habit in habits:
        checked = st.checkbox(habit.name, value=habit.is_done(today))
        if checked:
            habit.mark_done(today)
        else:
            habit.unmark_done(today)

    st.header("Summary")
    st.write("Total habits:", len(habits))
    done_count = sum(h.is_done(today) for h in habits)
    st.write("Completed today:", done_count)
    st.write("Total completions per habit:")
    for habit in habits:
        st.write(f"{habit.name}: {habit.count_done()}")

if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import time
import os

# Create a folder called data in the main project folder
DATA_FOLDER = "data"
if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

# Define CSV file paths for each part of the usability testing
CONSENT_CSV = os.path.join(DATA_FOLDER, "consent_data.csv")
DEMOGRAPHIC_CSV = os.path.join(DATA_FOLDER, "demographic_data.csv")
TASK_CSV = os.path.join(DATA_FOLDER, "task_data.csv")
EXIT_CSV = os.path.join(DATA_FOLDER, "exit_data.csv")


def save_to_csv(data_dict, csv_file):
    # Convert dict to DataFrame with a single row
    df_new = pd.DataFrame([data_dict])
    if not os.path.isfile(csv_file):
        # If CSV doesn't exist, write with headers
        df_new.to_csv(csv_file, mode='w', header=True, index=False)
    else:
        # Else, we need to append without writing the header!
        df_new.to_csv(csv_file, mode='a', header=False, index=False)


def load_from_csv(csv_file):
    if os.path.isfile(csv_file):
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame()


def main():
    st.title("Usability Testing Tool")

    home, consent, demographics, tasks, exit, report = st.tabs(
        ["Home", "Consent", "Demographics", "Task", "Exit Questionnaire", "Report"])

    with home:
        st.header("Introduction")
        st.write("""
        Welcome to the Usability Testing Tool for HCI.

        In this app, you will:
        1. Provide consent for data collection.
        2. Fill out a short demographic questionnaire.
        3. Perform a specific task (or tasks).
        4. Answer an exit questionnaire about your experience.
        5. View a summary report (for demonstration purposes).
        """)

    with consent:
        st.header("Consent Form")

        st.write("Please read the consent form below and confirm your agreement to the study.")
        st.write("Consent agreement:")
        st.markdown(
            """
            - I understand the purpose of this usability study
            - I understand that I'm not being tested, but I am testing the 'product'.
            - I am aware that my data will be collected solely for research and improvement purposes.
            - I can withdraw from this study at any time.
            """)

        consent_given = st.checkbox("I agree to the terms above.")

        if st.button("Submit Consent"):
            if not consent_given:
                st.warning("Please agree to the consent terms before proceeding.")
            else:
                # Save the consent acceptance time

                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "consent_given": consent_given
                }
                save_to_csv(data_dict, CONSENT_CSV)
                st.success("Consent submitted.")

    with demographics:
        st.header("Demographic Questionnaire")

        with st.form("demographic_form"):
            name = st.text_input("Name (optional):")
            age = st.number_input("Age:", 18, 100)
            occupation = st.text_input("Occupation:")
            familiarity = st.selectbox("Familiarity with similar tools:", ["Not Familiar", "Somewhat Familiar", "Very Familiar"])


            submitted = st.form_submit_button("Submit Demographics")
            if submitted:
                if not consent_given:
                    st.warning("Please agree to the consent terms before proceeding.")
                else:
                    data_dict = {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "name": name,
                        "age": age,
                        "occupation": occupation,
                        "familiarity": familiarity
                    }
                    save_to_csv(data_dict, DEMOGRAPHIC_CSV)
                    st.success("Demographic questionnaire submitted.")

    with tasks:
        st.header("Task Page")
        st.write("Please select a task and record your experience completing it.")

        # For this template, we assume there's only one task, in project 3, we will have to include the actual tasks
        selected_task = st.selectbox("Select Task", ["Task 1: Exchange Rate", "Task 2: Conversion", "Task 3: Chili", "Task 4: Requests"])

        if selected_task == "Task 1: Exchange Rate":
            st.write("Task Description: Find the exchange rate for USD/TJS, and LTC/CNH.")
        elif selected_task == "Task 2: Conversion":
            st.write("Task Description: Hide the labels for the input boxes of the website. Then, convert USD $121 to CAD.")
        elif selected_task == "Task 3: Chili":
            st.write("Task Description: Find the town named Chili.")
        elif selected_task == "Task 4: Requests":
            st.write("Task Description: Check the usage of the api requests made within the current day cycle.")



        # Track success, completion time, etc.
        start_button = st.button("Start Task Timer")
        if start_button:
            if not consent_given:
                st.warning("Please agree to the consent terms before proceeding.")
            else:
                st.session_state["start_time"] = time.time()
                st.info("Task has been started. When you complete the task, please click the 'Stop Task Timer' button and continue")

        stop_button = st.button("Stop Task Timer")
        if stop_button and "start_time" in st.session_state:
            duration = time.time() - st.session_state["start_time"]
            st.session_state["task_duration"] = duration
            st.success("Task has been completed in {:.2f} seconds.".format(duration))


        success = st.radio("Was the task completed successfully?", ["Yes", "No", "Partial"])
        notes = st.text_area("Observer Notes")

        if st.button("Save Task Results"):
            if not consent_given:
                st.warning("Please agree to the consent terms before proceeding.")
            else:
                duration_val = st.session_state.get("task_duration", None)

                data_dict = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "task_name": selected_task,
                    "success": success,
                    "duration_seconds": duration_val if duration_val else "",
                    "notes": notes
                }
                save_to_csv(data_dict, TASK_CSV)
                st.success("Task results saved.")


            # Reset any stored time in session_state if you'd like
            if "start_time" in st.session_state:
                del st.session_state["start_time"]
            if "task_duration" in st.session_state:
                del st.session_state["task_duration"]

    with exit:
        st.header("Exit Questionnaire")

        with st.form("exit_form"):
            # TODO: likert scale or other way to have an exit questionnaire

            satisfaction = st.slider("Overall Satisfaction (1 = Very Low, 5 = Very High", 1, 5)
            difficulty = st.slider("Overall Difficulty (1 = Very Easy, 5 = Very Hard)", 1, 5)
            open_feedback = st.text_area("Additional Feedback or comments:")

            submitted_exit = st.form_submit_button("Submit Exit Questionnaire")
            if submitted_exit:
                if not consent_given:
                    st.warning("Please agree to the consent terms before proceeding.")
                else:
                    data_dict = {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "satisfaction": satisfaction,
                        "difficulty": difficulty,
                        "open_feedback": open_feedback
                    }
                    save_to_csv(data_dict, EXIT_CSV)
                    st.success("Exit questionnaire data saved.")

    with report:
        if not consent_given:
            st.error("You can't access this page without agreeing to the consent terms. Please agree to the consent terms before proceeding.")
        else:
            st.header("Usability Report - Aggregated Results")

            st.write("**Consent Data**")
            consent_df = load_from_csv(CONSENT_CSV)
            if not consent_df.empty:
                # st.dataframe(consent_df)
                st.write("Total Consent Forms: {}".format(len(consent_df)))
            else:
                st.info("No consent data available yet.")

            st.write("**Demographic Data**")
            demographic_df = load_from_csv(DEMOGRAPHIC_CSV)
            if not demographic_df.empty:
                # st.dataframe(demographic_df)
                st.bar_chart(demographic_df, x="familiarity", y="occupation", color="occupation")
            else:
                st.info("No demographic data available yet.")

            st.write("**Task Performance Data**")
            task_df = load_from_csv(TASK_CSV)
            if not task_df.empty:
                # st.dataframe(task_df)
                st.bar_chart(task_df, x="task_name", y="success")
            else:
                st.info("No task data available yet.")

            st.write("**Exit Questionnaire Data**")
            exit_df = load_from_csv(EXIT_CSV)
            if not exit_df.empty:
                # st.dataframe(exit_df)
                st.bar_chart(exit_df, x="satisfaction", y="difficulty", color="difficulty")
            else:
                st.info("No exit questionnaire data available yet.")

            # Example of aggregated stats (for demonstration only)
            if not exit_df.empty:
                st.subheader("Exit Questionnaire Averages")
                avg_satisfaction = exit_df["satisfaction"].mean()
                avg_difficulty = exit_df["difficulty"].mean()
                st.write(f"**Average Satisfaction**: {avg_satisfaction:.2f}")
                st.write(f"**Average Difficulty**: {avg_difficulty:.2f}")




if __name__ == "__main__":
    main()
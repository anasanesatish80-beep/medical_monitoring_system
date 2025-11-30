
import json  # For handling patient data in JSON format
import logging  # For logging system events and alerts
from google.adk.agents import Agent  # Base Agent class from Google ADK
from google.adk.models import Gemini  # Gemini LLM model from Google ADK
from utils.data_loader import load_patient_data  # Function to load patient data from JSON file
from tools.alert_tool import check_alerts  # Function to check patient alerts
from utils import visualization  # Visualization utilities for plotting
import time  # For adding delays in the monitoring loop
import threading  # For parallel agent execution
import os  # For environment variable access
from dotenv import load_dotenv  # For loading .env file



# Load environment variables from .env file
load_dotenv()

# Setup logging to file for observability and debugging
logging.basicConfig(filename='logs/agent_logs.log', level=logging.INFO)
logging.info("Medical Monitoring System Started")


# Load patient data from the JSON file
# This simulates real patient data for the monitoring system
patients_data = load_patient_data()
patients_json = json.dumps(patients_data)  # Convert to JSON string for tool compatibility


# Tool function to monitor patient vitals and generate alerts
# Accepts a JSON string of patient data, checks each patient for alert conditions,
# and returns a summary of alerts for all patients.
def monitor_patient_tool(patients_json: str):
    patients = json.loads(patients_json)  # Parse JSON string to Python list
    alert_summary = {}  # Dictionary to store alerts for each patient
    for patient in patients:
        alerts = check_alerts(patient)  # Check for alert conditions (fever, BP, etc.)
        if alerts:
            alert_summary[patient["name"]] = alerts  # Add alerts to summary if any
    return alert_summary  # Return dictionary of patient alerts



# Create the LLM‑powered root agent with Gemini
# The agent is configured with the Gemini model and the monitoring tool
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Get API key from environment
gemini_model = Gemini(model="gemini-2.5-flash-lite", api_key=GOOGLE_API_KEY)  # Pass API key to Gemini

root_agent = Agent(
    model=gemini_model,  # Assign Gemini model to agent
    name="medical_monitoring_bot",  # Agent name
    description="Monitors patient vitals and generates alerts with explanations.",  # Agent description
    tools=[monitor_patient_tool]  # List of tools (functions) agent can use
)


# List to store alert history for each monitoring run
alert_history = []



# Parallel agent execution: monitor each patient in a separate thread
def monitor_patient_thread(patient, alert_summary):
    """
    Thread target function to check alerts for a single patient and update shared alert_summary.
    """
    alerts = check_alerts(patient)
    if alerts:
        alert_summary[patient["name"]] = alerts

# Main monitoring loop
# Runs the monitoring process 3 times to simulate periodic checks
for i in range(3):
    print(f"\n--- Monitoring Run #{i+1} ---")  # Indicate monitoring run number
    alert_summary = {}  # Shared dictionary for alerts
    threads = []
    # Start a thread for each patient
    for patient in patients_data:
        t = threading.Thread(target=monitor_patient_thread, args=(patient, alert_summary))
        threads.append(t)
        t.start()
    # Wait for all threads to finish
    for t in threads:
        t.join()
    alert_history.append(alert_summary)  # Store alerts for visualization

    # Print alerts for each patient in this run
    if alert_summary:
        for patient, issues in alert_summary.items():
            print(f"[ALERT] {patient}: {', '.join(issues)}")  # Print alert details
    else:
        print("All patients are stable.")  # No alerts for any patient

    # Human-readable summary of alerts (LLM call commented out)
    print("\n=== Human-Readable Alert Summary ===")
    if alert_summary:
        for patient, issues in alert_summary.items():
            print(f"{patient}: {', '.join(issues)}")  # Print summary for each patient
    else:
        print("All patients are stable.")  # Print if no alerts

    time.sleep(1)  # Wait 1 second before next run



# Visualize the total alert counts for each patient across all runs
visualization.plot_alert_counts(alert_history)

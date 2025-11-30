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
import queue  # For agent-to-agent communication
# EvaluationAgent for agent-to-agent communication and evaluation


class EvaluationAgent:
    def __init__(self):
        self.received_alerts = []  # Store received alerts for evaluation

    def receive_alerts(self, alerts):
        """
        Receive alerts from other agents and log them.
        """
        self.received_alerts.append(alerts)
        print("[EvaluationAgent] Received alerts for evaluation.")

    def evaluate(self):
        """
        Simple evaluation: count total alerts received.
        """
        total_patients = sum(len(alerts) for alerts in self.received_alerts)
        print(f"[EvaluationAgent] Total patients with alerts (all runs): {total_patients}")



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





# Function to run monitoring using root_agent (LLM-powered)
def monitor_with_root_agent(patients_json, alert_summary):
    """
    Uses root_agent to process patient data and update alert_summary.
    """
    result = root_agent.tools[0](patients_json)
    for patient, alerts in result.items():
        alert_summary[patient] = alerts


# Instantiate EvaluationAgent and a communication queue
evaluation_agent = EvaluationAgent()
alert_queue = queue.Queue()


# Main monitoring loop
# Runs the monitoring process 3 times to simulate periodic checks
for i in range(3):
    print(f"\n--- Monitoring Run #{i+1} ---")  # Indicate monitoring run number
    alert_summary = {}  # Shared dictionary for alerts

    # Use root_agent to process all patients in one step (LLM-powered)
    monitor_with_root_agent(patients_json, alert_summary)
    alert_history.append(alert_summary)  # Store alerts for visualization

    # Agent-to-agent communication: send alerts to EvaluationAgent via queue
    alert_queue.put(alert_summary)
    # EvaluationAgent receives alerts
    if not alert_queue.empty():
        evaluation_agent.receive_alerts(alert_queue.get())

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

# After monitoring runs, evaluate agent performance
evaluation_agent.evaluate()



# Visualize the total alert counts for each patient across all runs
visualization.plot_alert_counts(alert_history)

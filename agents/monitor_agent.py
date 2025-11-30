
# Import required libraries
from pydantic import Field  # For data validation and settings management
from typing import List, Dict  # For type annotations
from google.adk.agents import Agent  # Base Agent class from Google ADK
from tools.alert_tool import check_alerts  # Function to check patient alerts


# MonitorAgent class is responsible for monitoring patient vitals and generating alerts.
# Inherits from the base Agent class.
class MonitorAgent(Agent):
    name: str = "MonitorAgent"  # Name identifier for the agent
    patients: List[Dict] = Field(default_factory=list)  # List of patient records

    def __init__(self, patients=None, **data):
        """
        Initializes the MonitorAgent with a list of patients.
        Args:
            patients (list of dict, optional): List of patient records.
            **data: Additional keyword arguments for the base Agent class.
        """
        super().__init__(**data)
        if patients:
            self.patients = patients  # Store patient data

    def run(self):
        """
        Checks each patient for alert conditions and returns a summary.
        Returns:
            dict: Dictionary mapping patient names to lists of alert strings.
        """
        patient_alerts = {}  # Dictionary to store alerts for each patient
        for patient in self.patients:
            alerts = check_alerts(patient)  # Check for alert conditions
            if alerts:
                patient_alerts[patient["name"]] = alerts  # Add alerts to summary if any
        return patient_alerts  # Return dictionary of patient alerts

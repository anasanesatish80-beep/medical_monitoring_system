
# Import required libraries
from pydantic import Field  # For data validation and settings management
from google.adk.agents import Agent  # Base Agent class from Google ADK


# AlertAgent class is responsible for handling and displaying patient alerts.
# Inherits from the base Agent class.
class AlertAgent(Agent):
    name: str = "AlertAgent"  # Name identifier for the agent

    def run(self, alerts):
        """
        Processes and prints alerts for each patient.
        Args:
            alerts (dict): Dictionary mapping patient names to lists of alert strings.
        Returns:
            int: Number of patients with alerts.
        """
        for patient, issues in alerts.items():
            print(f"[ALERT] {patient}: {', '.join(issues)}")  # Print alert details for each patient
        return len(alerts)  # Return count of patients with alerts

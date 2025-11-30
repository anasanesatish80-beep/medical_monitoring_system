
# Import required libraries
from pydantic import Field  # For data validation and settings management
from typing import List, Dict  # For type annotations
from google.adk.agents import Agent, LlmAgent  # Base Agent and LLM Agent classes
from agents.monitor_agent import MonitorAgent  # Monitor agent for patient vitals
from agents.alert_agent import AlertAgent  # Alert agent for patient alerts
from utils.data_loader import load_patient_data  # Function to load patient data
import logging  # For logging system events

# Setup logging to file for observability and debugging
logging.basicConfig(filename='logs/agent_logs.log', level=logging.INFO)




# ExplanationAgent class is responsible for generating human-readable summaries of patient alerts.
# Inherits from the LlmAgent class.
class ExplanationAgent(LlmAgent):
    name: str = "ExplanationAgent"  # Name identifier for the agent

    def run(self, patient_alerts):
        """
        Generates a human-readable summary of patient alerts.
        Args:
            patient_alerts (dict): Dictionary mapping patient names to lists of alert strings.
        Returns:
            str: Human-readable summary of patient health alerts.
        """
        if not patient_alerts:
            return "All patients are stable. No alerts."  # No alerts to summarize
        explanation = "Patient Health Summary:\n"  # Header for summary
        for patient, issues in patient_alerts.items():
            explanation += f"{patient}: {', '.join(issues)}\n"  # Add each patient's alerts
        return explanation  # Return the summary string

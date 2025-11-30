
# Import required libraries
from pydantic import Field  # For data validation and settings management
from typing import List, Dict  # For type annotations
from google.adk.agents import Agent  # Base Agent class from Google ADK
from agents.monitor_agent import MonitorAgent  # Monitor agent for patient vitals
from agents.alert_agent import AlertAgent  # Alert agent for patient alerts
from agents.explanation_agent import ExplanationAgent  # Explanation agent for summaries
from utils.data_loader import load_patient_data  # Function to load patient data
import logging  # For logging system events

# Setup logging to file for observability and debugging
logging.basicConfig(filename='logs/agent_logs.log', level=logging.INFO)


# RootAgent class coordinates the monitoring, alerting, and explanation agents.
# Inherits from the base Agent class.
class RootAgent(Agent):
    name: str = "RootAgent"  # Name identifier for the agent
    patients: List[Dict] = Field(default_factory=list)  # List of patient records
    monitor_agent: MonitorAgent = Field(default_factory=lambda: MonitorAgent())  # Agent for monitoring
    alert_agent: AlertAgent = Field(default_factory=lambda: AlertAgent())  # Agent for alerts
    explanation_agent: ExplanationAgent = Field(default_factory=lambda: ExplanationAgent())  # Agent for explanations
    alert_history: List[Dict] = Field(default_factory=list)  # History of alerts

    def __init__(self, **data):
        """
        Initializes the RootAgent and its sub-agents.
        Loads patient data if not provided.
        Args:
            **data: Additional keyword arguments for the base Agent class.
        """
        super().__init__(**data)
        if not self.patients:
            self.patients = load_patient_data()  # Load patient data from file
        self.monitor_agent = MonitorAgent(self.patients)  # Initialize monitor agent
        self.alert_agent = AlertAgent()  # Initialize alert agent
        self.explanation_agent = ExplanationAgent()  # Initialize explanation agent
        logging.info(
            "RootAgent initialized with patients: %s", [p["name"] for p in self.patients]
        )

    def run(self):
        """
        Runs the monitoring, alerting, and explanation process for all patients.
        Prints and logs the results.
        """
        # Run monitoring agent to get alerts
        alerts = self.monitor_agent.run()
        if alerts:
            self.alert_agent.run(alerts)  # Print alerts
            self.alert_history.append(alerts)  # Store alerts in history

        # Prepare prompt for Gemini LLM summary
        if alerts:
            prompt_text = f"Summarize the following patient alerts in human-readable form: {alerts}"
            llm_response = self.complete(prompt_text)  # Use Agent.complete() for LLM summary
            explanation = llm_response.output_text  # Extract summary text
        else:
            explanation = "All patients are stable."  # No alerts to summarize

        print("\n=== Human-Readable Report ===")
        print(explanation)  # Print summary
        logging.info("Run completed. Alerts: %s", alerts)  # Log run details
        print(f"Total patients with alerts: {len(alerts)}\n")  # Print count

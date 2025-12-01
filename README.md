# Clinical Alert AI: Smart Patient Monitoring System

## Overview
Clinical Alert AI is an intelligent multi-agent system designed to automate the monitoring of patient vitals in hospitals. It uses AI-powered agents to analyze patient data, generate alerts for dangerous conditions, and provide human-readable summaries and visualizations to improve patient safety and staff efficiency.

## Features
- **Multi-agent architecture:** Root agent powered by Gemini LLM, with monitoring, alert, explanation, and evaluation agents.
- **Parallel patient monitoring:** Uses threading for efficient, real-time analysis.
- **Custom tools:** Detects high fever, blood pressure, blood sugar, and low oxygen.
- **Agent-to-agent communication:** Alerts are sent to an evaluation agent for logging and performance analysis.
- **Visualization:** Plots total alert counts per patient.
- **Logging:** Tracks system events and alerts for observability.
- **Configurable:** Uses `.env` for API keys and settings.

## Problem Statement
Hospitals need to continuously monitor patient vitals to detect dangerous conditions early and prevent adverse events. Manual monitoring is error-prone and resource-intensive, especially with many patients. Automating this process improves patient safety, reduces staff workload, and enables faster intervention.

## Why Agents?
Agents autonomously monitor, analyze, and respond to patient data in real time. Multi-agent systems allow for modular, scalable, and parallel processing—handling multiple patients, alerting staff, and generating explanations without human intervention.

## Architecture
- **Root Agent:** Coordinates monitoring, alerting, and explanation.
- **Monitor Agent:** Checks patient data for dangerous conditions.
- **Alert Agent:** Notifies staff of detected issues.
- **Explanation Agent:** Summarizes alerts in human-readable form.
- **Evaluation Agent:** Receives alerts and evaluates agent performance.
- **Visualization Module:** Plots alert trends.

## Demo
Run the following command to simulate monitoring:
```bash
python main.py
```
- The system prints alerts for dangerous conditions, summarizes them, and visualizes alert counts.
- Alerts are sent to the evaluation agent, which reports total alerts across all runs.

## Technology Stack
- Python
- Google ADK & Gemini LLM
- Matplotlib & Seaborn (visualization)
- Threading (parallel execution)
- Logging
- dotenv (.env configuration)

## How to Run
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your `GOOGLE_API_KEY` in `.env`.
4. Run the project:
   ```bash
   python main.py
   ```

## If I Had More Time
- Integrate real-time data from hospital devices.
- Build a web dashboard for live monitoring.
- Add notification systems (SMS, email, paging).
- Implement advanced analytics and predictive alerts.
- Add role-based access and security.
- Deploy as a cloud or on-premises service.
- Add agent-to-agent communication and evaluation protocols.

## License
This project uses only open-source and royalty-free components. See individual libraries for their licenses.

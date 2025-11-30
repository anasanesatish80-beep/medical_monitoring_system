
# Import required libraries for visualization
import matplotlib.pyplot as plt  # For plotting graphs
import seaborn as sns  # For enhanced visual styles

# Function to plot total alert counts for each patient
# Takes alert history from multiple monitoring runs and visualizes the data
def plot_alert_counts(alert_history):
    patient_counts = {}  # Dictionary to store total alert counts per patient
    # Aggregate alert counts for each patient across all runs
    for run_alerts in alert_history:
        for patient, alerts in run_alerts.items():
            patient_counts[patient] = patient_counts.get(patient, 0) + len(alerts)
    # If no alerts, print message and exit
    if not patient_counts:
        print("No alerts to plot.")
        return
    # Create bar plot of alert counts
    plt.figure(figsize=(8,5))
    sns.barplot(x=list(patient_counts.keys()), y=list(patient_counts.values()))
    plt.title("Total Alerts per Patient")
    plt.ylabel("Number of Alerts")
    plt.xlabel("Patient")
    plt.show()  # Display the plot

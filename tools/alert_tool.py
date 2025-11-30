
# Function to check alert conditions for a single patient
# Evaluates temperature, blood pressure, blood sugar, and oxygen levels
# Returns a list of alert strings for any dangerous conditions detected
def check_alerts(patient):
    alerts = []  # List to store alert messages
    # Check for high fever
    if patient["temperature"] > 100.4:
        alerts.append("High fever")
    # Check for high blood pressure
    bp = patient["blood_pressure"].split("/")  # Split BP into systolic/diastolic
    if int(bp[0]) > 140 or int(bp[1]) > 90:
        alerts.append("High blood pressure")
    # Check for high blood sugar
    if patient["blood_sugar"] > 180:
        alerts.append("High blood sugar")
    # Check for low oxygen level
    if patient["oxygen"] < 90:
        alerts.append("Low oxygen level")
    return alerts  # Return list of alerts

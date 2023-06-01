import RPi.GPIO as GPIO

# Set up GPIO and LDR pin
GPIO.setmode(GPIO.BCM)
LDR_PIN = 18
GPIO.setup(LDR_PIN, GPIO.IN)

# Measure the baseline LDR reading
baseline_reading = GPIO.input(LDR_PIN)

# Continuously monitor LDR readings
while True:
    # Read the current LDR reading
    current_reading = GPIO.input(LDR_PIN)
    
    # Calculate the difference in readings
    reading_difference = current_reading - baseline_reading
    
    # Use the reading difference to estimate proximity or relative distance
    # You can define your own logic based on the specific behavior of your LDR sensor
    
    # Print the reading difference
    print("Reading Difference:", reading_difference)

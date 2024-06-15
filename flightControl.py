import numpy as np
import time


class PIDController:
    def __init__(self, kp, ki, kd):
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd
        self.previous_error = 0
        self.integral = 0

    def compute(self, error):
        self.integral += error
        derivative = error - self.previous_error
        output = self.Kp * error + self.Ki * self.integral + self.Kd * derivative
        self.previous_error = error
        return output


# flight control function
def flightControl(current_position, target_position, pid__controller):
    error = np.linalg.norm(np.array(target_position) - np.array(current_position))
    control_output = pid__controller.compute(error)
    return control_output


# sensor data integration (GPS)
def getCurrentPosition(x, y):
    return x, y


if __name__ == "__main__":

    # Initialize target coordinates and threshold distance
    target_coordinates = (100, 100)  # target coordinates
    threshold_distance = 1.0  # threshold distance to consider target reached
    reached_target = False

    # Initialize PID controller with example parameters
    pid_controller = PIDController(1.0, 0.1, 0.01)

    # Example autonomous navigation loop
    while not reached_target:
        curr_position = getCurrentPosition(10, 20)
        control_outputt = flightControl(curr_position, target_coordinates, pid_controller)

        # Apply control output to actuators (e.g., motors for drone control)
        # Placeholder: print control output (replace with actual actuator control logic)
        print(f"Control Output: {control_outputt}")

        # Check if target coordinates reached (example condition)
        if np.linalg.norm(np.array(curr_position) - np.array(target_coordinates)) < threshold_distance:
            reached_target = True

        # Sleep for a small-time interval (simulation of real-time operation)
        time.sleep(0.1)

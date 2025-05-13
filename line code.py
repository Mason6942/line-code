#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain and basic setup
brain = Brain()

# Motor configuration
left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
left_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
left_drive = MotorGroup(left_motor_a, left_motor_b)

right_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_drive = MotorGroup(right_motor_a, right_motor_b)

# Sensors
distance_sensor = Distance(Ports.PORT11)
line_tracker = Line(brain.three_wire_port.a)  # Make sure your line tracker is in port A

# Clear screen
wait(300, MSEC)
print("\033[2J")

def when_started():
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("Scanning...")

        # === LINE TRACKER CHECK ===
        if line_tracker.reflectivity() <  :  # Adjust threshold if needed
            brain.screen.set_cursor(2, 1)
            brain.screen.print("Line detected! Turning around...")

            # Spin 180 degrees (adjust time if needed)
            left_drive.spin(REVERSE, 50, PERCENT)
            right_drive.spin(REVERSE, 50, PERCENT)
            wait(1.2, SECONDS)

            left_drive.stop(BRAKE)
            right_drive.stop(BRAKE)
            wait(0.5, SECONDS)
            continue  # Skip the rest and start scanning again

        # Normal scanning motion
        left_drive.spin(FORWARD, 20, PERCENT)
        right_drive.spin(FORWARD, 20, PERCENT)
        wait(1, SECONDS)

        left_drive.stop()
        right_drive.stop()
        wait(0.1, SECONDS)

        distance_mm = distance_sensor.object_distance(DistanceUnits.MM)
        brain.screen.set_cursor(2, 1)
        brain.screen.print("Distance: " + str(distance_mm))

        if 0 < distance_mm < 400:
            brain.screen.set_cursor(3, 1)
            brain.screen.print("Target detected!")

            # Move forward
            left_drive.spin(REVERSE, 70, PERCENT)
            right_drive.spin(FORWARD, 70, PERCENT)
            wait(2.5, SECONDS)

            # Tiny reverse
            left_drive.spin(FORWARD, 50, PERCENT)
            right_drive.spin(REVERSE, 50, PERCENT)
            wait(1, SECONDS)

            # Final charge
            left_drive.spin(REVERSE, 100, PERCENT)
            right_drive.spin(FORWARD, 100, PERCENT)
            wait(2.5, SECONDS)

            left_drive.stop(BRAKE)
            right_drive.stop(BRAKE)
            brain.screen.set_cursor(4, 1)
            brain.screen.print("Attack complete.")
            wait(1, SECONDS)

        else:
            brain.screen.set_cursor(3, 1)
            brain.screen.print("No target. Keep scanning.")

        wait(0.3, SECONDS)

# Start the program
when_started()

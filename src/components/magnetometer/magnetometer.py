import smbus
import math
import time

# MPU6050 Registers
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_XOUT = 0x3B
ACCEL_YOUT = 0x3D
ACCEL_ZOUT = 0x3F
GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47

# MPU6050 I2C address
MPU6050_ADDR = 0x68

# MPU6050 sensitivity scale factor constants
ACCEL_SCALE_FACTOR = 16384.0
GYRO_SCALE_FACTOR = 131.0

# Open the I2C bus
bus = smbus.SMBus(1)

# Initialize MPU6050
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

def read_raw_data(register):
    # Read raw 16-bit value from the specified register address
    high = bus.read_byte_data(MPU6050_ADDR, register)
    low = bus.read_byte_data(MPU6050_ADDR, register + 1)
    value = (high << 8) + low

    # Convert the value to a signed 16-bit number
    if value > 32768:
        value = value - 65536

    return value

def calculate_angle(x, y):
    angle = math.atan2(y, x) * (180.0 / math.pi)
    if angle < 0:
        angle += 360.0
    return angle

def update_angles(gyro_x, gyro_y, gyro_z, dt):
    # Calculate change in angles based on gyroscope readings
    gyro_angle_x = gyro_x * dt
    gyro_angle_y = gyro_y * dt

    # Update current angles
    current_angle_x = gyro_angle_x + previous_angle_x
    current_angle_y = gyro_angle_y + previous_angle_y

    # Normalize angles to 0-360 range
    current_angle_x = current_angle_x % 360.0
    current_angle_y = current_angle_y % 360.0

    return current_angle_x, current_angle_y

# Initialize previous angles and timestamp
previous_angle_x = 0.0
previous_angle_y = 0.0
previous_time = time.time()

try:
    while True:
        # Read accelerometer data
        accel_x = read_raw_data(ACCEL_XOUT) / ACCEL_SCALE_FACTOR
        accel_y = read_raw_data(ACCEL_YOUT) / ACCEL_SCALE_FACTOR
        accel_z = read_raw_data(ACCEL_ZOUT) / ACCEL_SCALE_FACTOR

        # Read gyroscope data
        gyro_x = read_raw_data(GYRO_XOUT) / GYRO_SCALE_FACTOR
        gyro_y = read_raw_data(GYRO_YOUT) / GYRO_SCALE_FACTOR
        gyro_z = read_raw_data(GYRO_ZOUT) / GYRO_SCALE_FACTOR

        # Calculate time difference since last iteration
        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time

        # Update angles
        current_angle_x, current_angle_y = update_angles(gyro_x, gyro_y, gyro_z, dt)
        print("X Angle: {:.2f} degrees".format(current_angle_x))
        print("Y Angle: {:.2f} degrees".format(current_angle_y))
        print("--------------------")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("im outty")


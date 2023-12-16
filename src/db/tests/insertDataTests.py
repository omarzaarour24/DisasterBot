import os
import sys
import pytest

import math
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src','db')))
from insertData import ResQBotDatabase

@pytest.fixture
def resqbot_db():
    return ResQBotDatabase()  # Create an instance of ResQBotDatabase for testing

def test_add_bot(resqbot_db):
    # Prepare test data
    test_id = 1
    test_cordx = 1
    test_cordy = 2

    # Execute the method
    resqbot_db.add_bot(2, 0, 0)

    # Retrieve the added bot information
    # You would typically use database querying/mocking to verify the addition
def test_update_bot(resqbot_db):
    resqbot_db.add_bot(1,1,2)
    resqbot_db.update_bot(1,2,5)
    new_x, new_y =resqbot_db.get_latest_cords(1)

    # Assert the coordinates are updated
    assert new_x == 2
    assert new_y == 5

def test_add_survivor_location(resqbot_db):
    # Prepare test data
    test_id = 1
    test_robotid = 2
    test_cordx = 70
    test_cordy = 80
    timestamp = "2023-08-15 12:34:56"

    # Execute the method
    resqbot_db.add_survivor_location(test_id, test_robotid, test_cordx, test_cordy,timestamp)

    # Retrieve the added survivor location
    # You would typically use database querying/mocking to verify the addition



def test_add_bot_current_location(resqbot_db):
    # Prepare test data
    test_id = 1
    test_robotid = 2
    test_duration = 5
    test_duty_cycle = 0.6
    test_angle = 30

    # Execute the method
    resqbot_db.add_bot_current_location(test_id, test_robotid, test_duration, test_duty_cycle, test_angle)

    # Retrieve the added bot current location
    # You would typically use database querying/mocking to verify the addition

def test_add_obstacles(resqbot_db):
    # Prepare test data
    test_id = 1
    test_robotid = 2
    test_distance = 25
    test_relative_angle = 45
    test_robot_direction = 90

    # Execute the method
    resqbot_db.add_obstacles(test_id, test_robotid, test_distance, test_relative_angle, test_robot_direction)

    # Retrieve the added obstacle information
    # You would typically use database querying/mocking to verify the addition

def test_add_tts_message(resqbot_db):
    # Prepare test data
    test_id = 1
    test_robotid = 1
    test_message = "Hello, world!"
    test_language = "en"
    # Execute the method
    resqbot_db.add_tts_message(test_id, test_robotid, test_message, test_language)

    # Retrieve the added TTS message information
    # You would typically use database querying/mocking to verify the addition

def test_add_drive_command(resqbot_db):
    # Prepare test data
    test_id = 1
    test_command_string = "FORWARD"
    test_robotid = 1

    # Execute the method
    resqbot_db.add_drive_command(test_id, test_command_string, test_robotid)

    # Retrieve the added drive command information
    # You would typically use database querying/mocking to verify the addition


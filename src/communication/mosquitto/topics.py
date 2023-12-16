sensors = {
    "sensors": {
        "forward_ultrasonic": "sensor/fus",
        "backward_ultrasonic": "sensor/bus",
        "left_ultrasonic": "sensor/lus",
        "right_ultrasonic": "sensor/rus",
        "radar": "sensor/radar",
        "gyro": "sensor/gyro",
        "microphone": "sensor/microphone"
    }
}
commands = {
    "motor": {
        "manual_controls": "command/controls",
    },
    "enable": {
        "camera": "command/camera",
        "auto_drive": "command/autodrive",
        "radar": "command/radar"
    },
    "text": {
        "tts": "command/tts"
    },
}
notopics = {
    "nothing":{
        "nothing": "nothing"
    }
}
#items
# -> topics to subscribe to
#   -> desc : topic

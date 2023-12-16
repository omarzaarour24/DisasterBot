import psycopg2
import mathimport math
class ResQBotDatabase:
    def __init__(self):
        # Connect to the PostgreSQL database
        self.conn = psycopg2.connect(
            host="localhost",
            database="resQBot",
            user="postgres",
            port="69",
            password="0000"
        )
        self.cursor = self.conn.cursor()

    def __del__(self):
        # Close the connection
        self.conn.close()
        
    def get_latest_cords(self,id):
        query = "SELECT cordx, cordy FROM bot where id = %s ORDER BY id DESC"
        values = (id,)
        self.cursor.execute(query,values)
        cords = self.cursor.fetchone()
        if cords:
            return cords[0], cords[1]
        else:
            return 0, 0
        
    def calculate_distance(self,duration, duty_cycle):
        actual_speed = 100 * duty_cycle
        distance = actual_speed * duration
        return distance
    
    def calculate_new_position(self, distance, angle, id):
        start_x, start_y = self.get_latest_cords(str(id))
        # Convert the angle from degrees to radians
        angle_rad = math.radians(angle)

        # Calculate the change in x and y coordinates
        delta_x = distance * math.cos(angle_rad)
        delta_y = distance * math.sin(angle_rad)

        # Calculate the new coordinates
        new_x = start_x + delta_x
        new_y = start_y + delta_y

        return new_x, new_y

    def calculate_obstacle_position(self,distance, relative_angle, robot_direction,robotid):
        robot_x, robot_y= self.get_latest_cords(robotid)
        # Convert the angles from degrees to radians
        relative_angle_rad = math.radians(relative_angle)
        robot_direction_rad = math.radians(robot_direction)

        # Actual angle where the obstacle is located
        actual_angle_rad = robot_direction_rad + relative_angle_rad

        # Calculate the obstacle's coordinates
        obstacle_x = robot_x + distance * math.cos(actual_angle_rad)
        obstacle_y = robot_y + distance * math.sin(actual_angle_rad)

        return obstacle_x, obstacle_y

    def get_latest_cords(self,id):
        query = "SELECT cordx, cordy FROM bot where id = %s ORDER BY id DESC"
        values = (id,)
        self.cursor.execute(query,values)
        cords = self.cursor.fetchone()
        if cords:
            return cords[0], cords[1]
        else:
            return 0, 0
        
    def calculate_distance(self,duration, duty_cycle):
        actual_speed = 100 * duty_cycle
        distance = actual_speed * duration
        return distance
    
    def calculate_new_position(self, distance, angle, id):
        start_x, start_y = self.get_latest_cords(str(id))
        # Convert the angle from degrees to radians
        angle_rad = math.radians(angle)

        # Calculate the change in x and y coordinates
        delta_x = distance * math.cos(angle_rad)
        delta_y = distance * math.sin(angle_rad)

        # Calculate the new coordinates
        new_x = start_x + delta_x
        new_y = start_y + delta_y

        return new_x, new_y

    def calculate_obstacle_position(self,distance, relative_angle, robot_direction,robotid):
        robot_x, robot_y= self.get_latest_cords(robotid)
        # Convert the angles from degrees to radians
        relative_angle_rad = math.radians(relative_angle)
        robot_direction_rad = math.radians(robot_direction)

        # Actual angle where the obstacle is located
        actual_angle_rad = robot_direction_rad + relative_angle_rad

        # Calculate the obstacle's coordinates
        obstacle_x = robot_x + distance * math.cos(actual_angle_rad)
        obstacle_y = robot_y + distance * math.sin(actual_angle_rad)

        return obstacle_x, obstacle_y

    def update_bot(self, id, cordx, cordy):
        query = "UPDATE bot SET cordx = %s, cordy = %s WHERE id = %s"
        values = (cordx, cordy,id)
        values = (cordx, cordy,id)
        self.cursor.execute(query, values)
        self.conn.commit()  # Commit the changes
    
    def add_survivor_location(self, id, robotid, cordx, cordy,timestamp):
        query = "INSERT INTO survivor_locations (id, robotid, cordx, cordy, timestamp) VALUES (%s, %s, %s, %s,%s) ON CONFLICT (cordx, cordy) DO NOTHING"
        values = (id, robotid, cordx, cordy,timestamp)
        self.conn.commit()  # Commit the changes
    
    def add_survivor_location(self, id, robotid, cordx, cordy,timestamp):
        query = "INSERT INTO survivor_locations (id, robotid, cordx, cordy, timestamp) VALUES (%s, %s, %s, %s,%s) ON CONFLICT (cordx, cordy) DO NOTHING"
        values = (id, robotid, cordx, cordy,timestamp)
        self.cursor.execute(query, values)

    def add_bot(self, id, cordx, cordy):
        query = "INSERT INTO bot (id, cordx, cordy) VALUES (%s, %s, %s) ON CONFLICT (cordx, cordy) DO NOTHING ON CONFLICT (cordx, cordy) DO NOTHING"
        values = (id, cordx, cordy)
        self.cursor.execute(query, values)

    def add_bot_current_location(self, id, robotid,duration, duty_cycle,angle):
        distance=self.calculate_distance(duration, duty_cycle)
        new_x, new_y=self.calculate_new_position(distance,angle,id)
        query = "INSERT INTO bot_current_location (id, robotid, cordx, cordy) VALUES (%s, %s, %s, %s) ON CONFLICT (cordx, cordy) DO NOTHING"
        values = (id, robotid, new_x, new_y)
    def add_bot_current_location(self, id, robotid,duration, duty_cycle,angle):
        distance=self.calculate_distance(duration, duty_cycle)
        new_x, new_y=self.calculate_new_position(distance,angle,id)
        query = "INSERT INTO bot_current_location (id, robotid, cordx, cordy) VALUES (%s, %s, %s, %s) ON CONFLICT (cordx, cordy) DO NOTHING"
        values = (id, robotid, new_x, new_y)
        self.cursor.execute(query, values)
        self.update_bot(robotid,new_x, new_y)
        self.update_bot(robotid,new_x, new_y)

    def add_obstacles(self, id,robotid,distance,relative_angle,robot_direction):
        obstacle_x, obstacle_y = self.calculate_obstacle_position(distance, relative_angle, robot_direction,robotid)
        query = "INSERT INTO obstacles (id, robotid, cordx, cordy) VALUES (%s, %s, %s, %s) ON CONFLICT (cordx, cordy) DO NOTHING"
        values = (id, robotid, obstacle_x, obstacle_y)
        self.cursor.execute(query, values)
    def add_obstacles(self, id,robotid,distance,relative_angle,robot_direction):
        obstacle_x, obstacle_y = self.calculate_obstacle_position(distance, relative_angle, robot_direction,robotid)
        query = "INSERT INTO obstacles (id, robotid, cordx, cordy) VALUES (%s, %s, %s, %s) ON CONFLICT (cordx, cordy) DO NOTHING"
        values = (id, robotid, obstacle_x, obstacle_y)
        self.cursor.execute(query, values)

    def add_tts_message(self, id, robotid,message, language):
        query = "INSERT INTO tts_messages (id,robotid, message, language) VALUES (%s, %s, %s,%s)"
        values = (id, robotid,message, language)
    def add_tts_message(self, id, robotid,message, language):
        query = "INSERT INTO tts_messages (id,robotid, message, language) VALUES (%s, %s, %s,%s)"
        values = (id, robotid,message, language)
        self.cursor.execute(query, values)

    def add_drive_command(self, id, command_string, robotid):
        query = "INSERT INTO drive_commands (id, command_string, robotid) VALUES (%s, %s, %s) "
        values = (id, command_string, robotid)
    def add_drive_command(self, id, command_string, robotid):
        query = "INSERT INTO drive_commands (id, command_string, robotid) VALUES (%s, %s, %s) "
        values = (id, command_string, robotid)
        self.cursor.execute(query, values)

    def commit_changes(self):
        # Commit the changes
        self.conn.commit()
        print("Data added successfully.")

# # Create an instance of the ResQBotDatabase class
# # Create an instance of the ResQBotDatabase class
db = ResQBotDatabase()
# # # Call the methods to add data
# # db.add_survivor_location(55, 1, 50, -200)
# # db.add_survivor_location(44, 22, 99, -200)
# # db.add_survivor_location(15, 8, 66, 80)
# # # Call the methods to add data
# # db.add_survivor_location(55, 1, 50, -200)
# # db.add_survivor_location(44, 22, 99, -200)
# # db.add_survivor_location(15, 8, 66, 80)

# # # Update the "bot" table
# db.add_bot(1,1,2)
# db.update_bot(1,2,5)
# # test_id = 1
# test_robotid = 2
# test_distance = 25
# test_relative_angle = 45
# test_robot_direction = 90

# # Execute the method
# db.add_obstacles(test_id, test_robotid, test_distance, test_relative_angle, test_robot_direction)
# # # Update the "bot" table
db.add_bot(1,1,2)
# db.update_bot(1,2,5)
# # test_id = 1
# test_robotid = 2
# test_distance = 25
# test_relative_angle = 45
# test_robot_direction = 90

# # Execute the method
# db.add_obstacles(test_id, test_robotid, test_distance, test_relative_angle, test_robot_direction)

db.add_bot_current_location(1,1,2,2,3)
db.add_bot_current_location(2,1,4,2,3)
db.add_bot_current_location(3,1,8,1,5)

db.add_obstacles(1,1,14,30)
db.add_obstacles(2,1,3,30)
# Commit the changes and close the connection
db.commit_changes()

### Task 3: Managing Workout Sessions.

  ###importing all packages that was installed and, list is located in the requirements text file.

from flask import Flask, jsonify, request

from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from connection import connect_fit, Error

workout = Flask(__name__)
ma = Marshmallow(workout)

class Workoutschema(ma.Schema):
    id = fields.Int(dump_only = True)
    workout_type= fields.String(required=True)
    duration= fields.String(required=True)
    # members_id = fields.Int(dump_only=True)
    members_id = fields.Int(required=True)

    class Meta:
        fields = ("id", "workout_type", "duration", "members_id")

workout_schema = Workoutschema()
workouts_schema = Workoutschema(many = True)

@workout.route('/')

def home():
    return " Welcome to Rogers Fitness Center workout schedule"

### Created a fetch all functions for workout programs.

@workout.route('/workouts', methods = ['GET'])

def get_workout():
    conn=connect_fit()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary =True)

            query = "SELECT * FROM workoutsessions"

            cursor.execute(query)

            workout = cursor.fetchall()

        except Error as e:
            return jsonify ({"error": e})
        
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close() 
                return workouts_schema.jsonify(workout)

### Created a function to update for workout programs using the workout session id in URL to identify the program..


@workout.route("/workouts/<int:id>", methods = ['PUT']) # dynamic route that can change based off of different query parameters
def update_workout(id):
    try:
        workout_data = workout_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connect_fit()
    if conn is not None:
        try:
            cursor = conn.cursor()

            # Query to check if we even have this program in our database.
            check_query = "SELECT * FROM workoutsessions WHERE id = %s;"
            cursor.execute(check_query, (id,))
            workout = cursor.fetchone()
            if not workout:
                return jsonify({"error": "workout program was not found."}), 404
            
            # create updated program info tuple
            updated_workout = (workout_data['workout_type'], workout_data['duration'], workout_data['members_id'], id) 

            query = "UPDATE workoutsessions SET workout_type = %s, duration = %s, members_id = %s  WHERE id = %s;" 

            cursor.execute(query, updated_workout)
            conn.commit()

            return jsonify({'message': f"Successfully updated workout program {id}"}), 200
        except Error as e:
            return jsonify(e.messages), 500
        
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500
    
### Created a function to add new workout programs.

@workout.route("/workouts", methods = ['POST'])
def add_member():
    try:
        workout_data = workout_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connect_fit()
    if conn is not None:
        try:
            cursor = conn.cursor()

            #new workout program data
            new_program = (workout_data['workout_type'], workout_data['duration'], workout_data['members_id'])

            #query
            query = "INSERT INTO workoutsessions (workout_type,duration,members_id) VALUES (%s,%s,%s)"
            
            #excecute the query with new workout program data
            cursor.execute(query, new_program)
            conn.commit()

            return jsonify({'message': 'New workout program addedd successfully'}), 201
        
        except Error as e:
            return jsonify(e.messages), 500
        
        finally:
            cursor.close()
            conn.close() # ALWAYS BE SURE TO CLOSE YOUR CONNECTIONS WHEN YOU'RE FINISHED WITH A QUERY
        
    else:
        return jsonify ({'error': 'Database connection failed'}), 500
    



#####Implement a route to retrieve all workout sessions for a specific member.

    ###Created a function that uses the members id from the member table to execute all members  workout programs.

@workout.route('/workouts/<int:members_id>', methods = ['GET'])


def mem_workout(members_id):
    conn=connect_fit()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary =True)

            query = "SELECT * FROM workoutsessions WHERE members_id = %s"

            cursor.execute(query, (members_id,))

            workout = cursor.fetchall()

        except Error as e:
            return jsonify ({"error": e})
        
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close() 
                return workouts_schema.jsonify(workout)
            
if __name__ == '__main__':
    workout.run(debug=True)
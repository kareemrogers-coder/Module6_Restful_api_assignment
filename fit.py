#######Task2: Implementing CRUD Operations for Members

    ###importing all packages that was installed and, list is located in the requirements text file.


from flask import Flask, jsonify, request

from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from connection import connect_fit, Error

fit = Flask(__name__)
ma = Marshmallow(fit)

class Memberschema(ma.Schema):
    id = fields.Int(dump_only = True)
    member_name = fields.String(required=True)

    class Meta:
        fields = ("id", "member_name", "phone")

member_schema = Memberschema()
members_schema = Memberschema(many = True)

@fit.route('/')

def home():
    return " Welcome to Rogers Fitness Center"

### Created a fetch all functions for all members.

@fit.route('/members', methods = ['GET'])

def get_members():
    conn=connect_fit()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary =True)

            query = "SELECT * FROM members"

            cursor.execute(query)

            members = cursor.fetchall()

        except Error as e:
            return jsonify ({"error": e})
        
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close() # ALWAYS BE SURE TO CLOSE YOUR CONNECTIONS WHEN YOU'RE FINISHED WITH A QUERY
                return members_schema.jsonify(members)

# Created a add new memeber function.

@fit.route("/members", methods = ['POST'])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connect_fit()
    if conn is not None:
        try:
            cursor = conn.cursor()

            #new member data
            new_member = (member_data['member_name'], member_data['phone'])

            #query
            query = "INSERT INTO members (member_name,phone) VALUES (%s,%s)"
            
            #excecute the query with new member data
            cursor.execute(query, new_member)
            conn.commit()

            return jsonify({'message': 'New member addedd successfully'}), 201
        
        except Error as e:
            return jsonify(e.messages), 500
        
               
        finally:
            cursor.close()
            conn.close() # ALWAYS BE SURE TO CLOSE YOUR CONNECTIONS WHEN YOU'RE FINISHED WITH A QUERY
        
    else:
        return jsonify ({'error': 'Database connection failed'}), 500
    
 # created a PUT(updating) functions to use the members id to update the members profile.
   
@fit.route("/members/<int:id>", methods = ['PUT']) # dynamic route that can change based off of different query parameters
def update_member(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connect_fit()
    if conn is not None:
        try:
            cursor = conn.cursor()

            # Query to check if we even have this member in our database
            check_query = "SELECT * FROM members WHERE id = %s;"
            cursor.execute(check_query, (id,))
            member = cursor.fetchone()
            if not member:
                return jsonify({"error": "Member was not found."}), 404
            
            # create updated member info tuple
            updated_member = (member_data['member_name'], member_data['phone'],id)

            query = "UPDATE members SET member_name = %s, phone = %s WHERE id = %s;"

            cursor.execute(query, updated_member)
            conn.commit()

            return jsonify({'message': f"Successfully updated member {id}"}), 200
        except Error as e:
            return jsonify(e.messages), 500
        
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Database connection failed"}), 500

## Created a delete function wo remove members who all now longer with the gym.

@fit.route("/members/<int:id>", methods = ['DELETE'])
def delete_member(id):

    conn = connect_fit()
    if conn is not None:
        try:
            cursor = conn.cursor()

            check_query = "SELECT * FROM members WHERE id = %s;"
            cursor.execute(check_query, (id,))
            member = cursor.fetchone()
            if not member:
                return jsonify({"error": "member was not found"}), 404
            
            query = "DELETE FROM members WHERE id = %s;"
            cursor.execute(query, (id,))
            conn.commit()

            return jsonify({"message": f"Member {id} was successfully destroyed!"})
        except Error as e:
            return jsonify(e.messages), 500
        
        finally:
            cursor.close()
            conn.close()

    else:
        return jsonify({"error": "Database connection failed"}), 500

if __name__ == '__main__':
    fit.run(debug=True)

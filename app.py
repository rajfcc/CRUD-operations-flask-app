from flask import Flask,jsonify,request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/flaskApp'
mongo = PyMongo(app)

@app.route('/')
def home():
    return jsonify(message='Hello, Flask with MongoDB!')

# Read all users
@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    return jsonify(users=[{'id': str(user['_id']), 'name': user['name'],'age':user['age'],'sex':user['sex']} for user in users])

# Create a user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user_id = mongo.db.users.insert_one({'name': data['name'],'age': data['age'],'sex':data['sex']}).inserted_id
    new_user = mongo.db.users.find_one({'_id': user_id})
    return jsonify(user={'id': str(new_user['_id']), 'name': new_user['name'],'age': new_user['age'],'sex':new_user['sex']}), 201

# Read a single user by id
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = mongo.db.users.find_one({'_id': ObjectId(id)})
    if user:
        return jsonify(user={'id': str(user['_id']), 'name': user['name'],'age':user['age'],'sex':user['sex']})
    else:
        return jsonify(message='User not found'), 404
    
# Update a user by id
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.json
    result = mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': {'name': data['name'],'age':data['age'],'sex':data['sex']}})
    if result.matched_count > 0:
        updated_user = mongo.db.users.find_one({'_id': ObjectId(id)})
        return jsonify(user={'id': str(updated_user['_id']), 'name': updated_user['name'],'age':updated_user['age'],'sex':updated_user['sex']})
    else:
        return jsonify(message='User not found'), 404

# Delete a user by id
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    result = mongo.db.users.delete_one({'_id': ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify(message='User deleted')
    else:
        return jsonify(message='User not found'), 404

if __name__ == '__main__':
    app.run(debug=True)

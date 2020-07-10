from flask import Flask, jsonify, request
from prepare import prepare, prediction, load_model_R34
from firebase import firebase_init
from mysql_connect import mysql_init

storage = firebase_init()
mydb = mysql_init()
app = Flask(__name__)

model = load_model_R34("R34EP200")

@app.route('/', methods=['GET'])
def Hello():
    return "Server Running..."

@app.route('/insertdata', methods=['POST'])
def insert_data_mysql():
    new_img = request.get_json()
    member_id = new_img['Sid']
    Type = new_img['Type']
    img_name = new_img['imageName']
    Bin = new_img['Bin']
    mycursor = mydb.cursor()
    sql = "INSERT INTO bin VALUES (%s, %s, %s, %s, %s);"
    val = (None, img_name, Type, Bin, member_id)
    mycursor.execute(sql, val)
    mydb.commit()
    res = mycursor.rowcount, "record inserted."
    return jsonify({'data' : res})

@app.route('/imgclass', methods=['POST'])
def predi_():
    new_img = request.get_json()
    img_name = new_img['imageName']
    path = 'image/{}'.format(img_name)
    storage.child( path ).download('image.jpg')
    img = prepare('image.jpg')
    Class = prediction(model, img)
    return jsonify({'data' : Class })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
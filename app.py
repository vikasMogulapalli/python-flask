import os
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config.update(
    MYSQL_USER='root',
    MYSQL_PASSWORD='15Bunny484@',
    MYSQL_DB='test',
    MYSQL_HOST='localhost'
)

mysql = MySQL(app)

# Default route to serve index.html and data
@app.route('/')
def home():
    try:
        # Fetch data from MySQL
        with mysql.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM student")
            data = cursor.fetchall()
    except Exception as e:
        print(f"Error: {e}")
        data = []
        
    return render_template('index.html', data=data)

# Route to insert data
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        rollno = request.form['rollno']
        name = request.form['name']
        image = request.files['image']
        video = request.files['video']
        
        # Save the image to the uploads folder
        image_filename = f"{rollno}_{image.filename}"
        image_path = os.path.join('static/uploads/', image_filename)
        image.save(image_path)

        # Save the video to the video_uploads folder
        video_filename = f"{rollno}_{video.filename}"
        video_path = os.path.join('static/video_uploads/', video_filename)
        video.save(video_path)
        
        # Store the relative path in the database
        try:
            with mysql.connection.cursor() as cursor:
                cursor.execute("INSERT INTO student VALUES (%s, %s, %s, %s)", (name, rollno, f"/static/uploads/{image_filename}", f"/static/video_uploads/{video_filename}"))
                mysql.connection.commit()  # Commit the transaction
                print('Data successfully inserted')
        except Exception as e:
            print(f"Error: {e}")
        
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)

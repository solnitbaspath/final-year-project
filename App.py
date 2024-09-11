from flask import Flask, render_template, request, session, flash

import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/OfficerLogin')
def OfficerLogin():
    return render_template('OfficerLogin.html')


@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')


@app.route('/NewUser')
def NewUser():
    return render_template('NewUser.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash("you are successfully Login")
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/NewOfficer")
def NewOfficer():
    return render_template('NewOfficer.html')


@app.route("/newofficer", methods=['GET', 'POST'])
def newofficer():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        depart = "National Disaster Management Authority"
        username = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into officertb values('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + depart + "','" + username + "','" + password + "')")
        conn.commit()
        conn.close()
        flash("Record Saved!")

    return render_template('NewOfficer.html')


@app.route("/AOfficerInfo")
def AOfficerInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM officertb ")
    data = cur.fetchall()
    return render_template('AOfficerInfo.html', data=data)


@app.route("/AComplaintInfo")
def AComplaintInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM complainttb  ")
    data = cur.fetchall()
    return render_template('AComplaintInfo.html', data=data)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into regtb values('','" + name + "','" + mobile + "','" + email + "','" + address + "','" + username + "','" + password + "')")
        conn.commit()
        conn.close()
        flash("Record Saved!")

    return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            flash('Username or Password is wrong')
            return render_template('UserLogin.html', data=data)

        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and password='" + password + "'")
            data = cur.fetchall()
            flash("you are successfully logged in")
            return render_template('UserHome.html', data=data)


@app.route("/NewComplaint")
def NewComplaint():
    return render_template('NewComplaint.html', uname=session['uname'])


@app.route("/newcomplaint", methods=['GET', 'POST'])
def newcomplaint():
    if request.method == 'POST':
        import cv2
        uname = session['uname']
        depart = "National Disaster Management Authority"
        info = request.form['info']

        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)

        import torch
        import numpy as np
        # Load the model
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/exp2/weights/best.pt',
                               force_reload=True)
        # model.conf = 0.2
        # Set webcam input
        cam = cv2.VideoCapture("static/upload/" + savename)
        dd1 = 0
        dd2 = 0
        dd3 = 0
        dd4 = 0
        ret, img = cam.read()
        dd2 += 1

        # Perform object detection

        # print(results)

        try:
            results = model(img)
            # Access the detection results
            class_names = ['flood', 'level 0', 'level 1', 'level 10', 'level 11', 'level 2', 'level 3', 'level 4',
                           'level 5', 'level 6', 'level 7', 'level 8',
                           'level 9']  # List of class names in the order corresponding to the model's output

            # Assuming results contains bounding box coordinates and class indices
            bounding_boxes = results.xyxy[0]  # Assuming the first image in results
            class_indices = bounding_boxes[:, -1].int().tolist()  # Extracting class indices
            # Mapping class indices to class names
            prediction_names = [class_names[idx] for idx in class_indices]
            # Printing prediction names
            print(prediction_names[0])

            if prediction_names[0] == "level 0":
                session["out"] = "Normal"
            else:
                session["out"] = prediction_names[0]



        except:
            pass

        if session['out'] == "Normal":

            flash("Normal")
            cv2.imshow("Output", np.squeeze(results.render()))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return render_template('NewComplaint.html', uname=session['uname'])
        else:
            cv2.imshow("Output", np.squeeze(results.render()))
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
            cursor = conn.cursor()
            cursor.execute("SELECT  *  FROM regtb where  username='" + uname + "'")
            data = cursor.fetchone()

            if data:
                mobile = data[2]

            else:
                return 'Incorrect username / password !'

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into complainttb values('','" + uname + "','" + mobile + "','" + depart + "','" + info + "','" + savename + "','','waiting','','','" +
                session["out"] + "')")
            conn.commit()
            conn.close()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM complainttb where username='" + uname + "'  ")
            data = cur.fetchall()
            flash('Complaint Post Successfully!')
            return render_template('UComplaintInfo.html', data=data)



        # Press 'q' or 'Esc' to quit
        #if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1) == 27):
            #break

        # Close the camera









@app.route("/UComplaintInfo")
def UComplaintInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM complainttb where username='" + session['uname'] + "' and Status='waiting' ")
    data = cur.fetchall()
    return render_template('UComplaintInfo.html', data=data)


@app.route("/UActionInfo")
def UActionInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM complainttb where username='" + session['uname'] + "' and Status !='waiting' ")
    data = cur.fetchall()
    return render_template('UActionInfo.html', data=data)


@app.route("/officerlogin", methods=['GET', 'POST'])
def officerlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['oname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from officertb where username='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:
            flash('Username or Password is wrong')
            return render_template('OfficerLogin.html', data=data)

        else:
            session['depart'] = data[5]
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM officertb where username='" + username + "' and password='" + password + "'")
            data = cur.fetchall()
            flash("you are successfully logged in")
            return render_template('OfficerHome.html', data=data)


@app.route("/OfficerHome")
def OfficerHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM officertb where username='" + session['oname'] + "' ")
    data = cur.fetchall()
    return render_template('OActionInfo.html', data=data)


@app.route("/OActionInfo")
def OActionInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM complainttb where Department='" + session['depart'] + "' and Status ='completed' ")
    data = cur.fetchall()
    return render_template('OActionInfo.html', data=data)


@app.route("/OComplaintInfo")
def OComplaintInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM complainttb where Department='" + session['depart'] + "' and Status !='completed' ")
    data = cur.fetchall()
    return render_template('OComplaintInfo.html', data=data)


@app.route("/action")
def action():
    id = request.args.get('id')
    session["cid"] = id

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
    cursor = conn.cursor()
    cursor.execute("SELECT  *  FROM complainttb where  id='" + id + "'")
    data = cursor.fetchone()

    if data:
        mobile = data[2]

    else:
        return 'Incorrect username / password !'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM complainttb where id='" + id + "' ")
    data = cur.fetchall()
    return render_template('Action.html', data=data)


@app.route("/actioninfo", methods=['GET', 'POST'])
def actioninfo():
    if request.method == 'POST':
        act = request.form['act']
        ainfo = request.form['ainfo']
        oname = session['oname']

        import random
        file = request.files['file']
        fnew = random.randint(1111, 9999)
        savename = str(fnew) + ".png"
        file.save("static/upload/" + savename)

        id = session["cid"]

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM complainttb where  id='" + id + "'")
        data = cursor.fetchone()

        if data:
            mobile = data[2]
        else:
            return 'Incorrect username / password !'
        msg = "Your Complaint Action Info" + ainfo
        sendmsg(mobile, msg)

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1flooddb')
        cursor = conn.cursor()
        cursor.execute(
            "update   complainttb set Action='" + ainfo + "',Status='" + act + "' , OfficerName='" + oname + "',Cimage='"+savename+"' where id='" + id + "'")
        conn.commit()
        conn.close()

        flash("Action Info Update successfully")

        return render_template('OActionInfo.html')



def sendmsg(targetno,message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

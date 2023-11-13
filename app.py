# flask app.py file
from flask import Flask, request, jsonify, render_template
import os
import g4f
import matplotlib.pyplot as plt
import cv2
import easyocr
from pylab import rcParams
from werkzeug.utils import secure_filename
from IPython.display import Image
import PyPDF2 as pdf

app = Flask(__name__)
users = [
    {
        'name': 'John',
        'email': 'john@abc.com',
        'password': 'john123'
    },
    {
        'name': 'Smith',
        'email': 'smith@abc.com',
        'password': 'smith123'
    },
]





@app.route('/')
def index():
    return render_template("about.html")

# @app.route('/signup', methods=['GET','POST'])
# def signup(methods=['POST']):
#     return render_template("signup.html")
#     # request_data = request.get_json()
#     # new_user = {
#     #             'name': request_data['name'],
#     #             'email': request_data['email'],
#     #             'password': request_data['password']
#     #             }
#     # users.append(new_user)
#     return render_template("signup.html")



global new

@app.route('/upload_image_route', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part in the request'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file in the root folder
    filename_root = secure_filename(file.filename)
    filepath_root = os.path.join(app.root_path, filename_root)
    file.save(filepath_root)

    # Save the file in the /tmp folder
    filename_tmp = secure_filename(file.filename)
    filepath_tmp = os.path.join('tmp', filename_tmp)
    file.save(filepath_tmp)

    # Process the file
    rcParams['figure.figsize'] = 8, 16
    reader = easyocr.Reader(['en'])
    Image(filepath_root)  # Displaying the image from the root folder
    output = reader.readtext(filepath_root)

    new = ''
    total_len = len(output)
    for x in range(total_len):
        new += output[x][1] + ' '

    #return jsonify({'new': new})
    sumtext = get_summary(new)
     

    print (sumtext)
    split_response = sumtext.split("Using Bing provider")
    #split_response[1]
    #converte split_response[0] to string
    a = str(split_response[0])
    data = {'message' : a}
    return render_template('show.html', data = data)
    #return jsonify({sumtext})


@app.route('/upload_pdf_route', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No pdf part in the request'}), 400

    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the file in the root folder
    filename_root = secure_filename(file.filename)
    filepath_root = os.path.join(app.root_path, filename_root)
    file.save(filepath_root)

    # Save the file in the /tmp folder
    filename_tmp = secure_filename(file.filename)
    filepath_tmp = os.path.join('tmp', filename_tmp)
    file.save(filepath_tmp)

    # Process the file
    # rcParams['figure.figsize'] = 8, 16
    # reader = easyocr.Reader(['en'])
    # Image(filepath_root)  # Displaying the image from the root folder
    # output = reader.readtext(filepath_root)
    f = open(filepath_root,'rb')
    pdf_reader = pdf.PdfReader(f)
    pdf_reader.pages
    len(pdf_reader.pages)
    page_one = pdf_reader.pages[0]
    page_one_text = page_one.extract_text()
    #type(page_one_text)

    # new = ''
    # total_len = len(output)
    # for x in range(total_len):
    #     new += output[x][1] + ' '

    #return jsonify({'new': new})
    sumtext = get_summary(page_one_text)
    print (sumtext)
    split_response = sumtext.split("Using Bing provider")
    #split_response[1]
    #converte split_response[0] to string
    a = str(split_response[0])
    data = {'message' : a}
    return render_template('show.html', data = data)

#@app.route('/summary_route', methods=['POST'])
def get_summary(new):

    g4f.debug.logging = True  # Enable logging
    g4f.check_version = False  # Disable automatic version checking
    response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    #provider=g4f.Provider.Aichat,
    messages=[{"role": "user", "content": new}],
    )  # Alternative model setting

    #return response
    summary = response
    #return jsonify({'summary': summary})
    return summary

@app.route('/signup', methods=['GET','POST'])
def signup():
    return render_template('signup.html')


@app.route('/signupmethod', methods=['GET','POST'])
def signupmethod():
    
    #name = request.form['name']
    new_user = {
                'name': request.form['name'],
                'email': request.form['email'],
                'password': request.form['password']
                }
    users.append(new_user)

    return render_template('signin.html')


@app.route('/signin', methods=['GET','POST'])
def signin():
    return render_template('signin.html')


@app.route('/signinmethod', methods=['GET','POST'])
def signinmethod():
    
    #name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    for user in users:
        if user['email'] == email and user['password'] == password:
            #return jsonify({'message': 'success'})
            data = {'message' : 'success'}
            return render_template('signinstatus.html', data = {'message' : 'success'})
    #return jsonify({'message': 'failure'})
    data = {'message' : 'failure'}
    return render_template('signinstatus.html', data = {'message' : 'failure'} )
#return render_template('index.html', prediction_text=str(result))


@app.route('/showusers', methods=['GET'])
def showusers():
    un=[]
    ue=[]
    cnt = 0
    for user in users:
        cnt+=1
        uname = user['name']
        un.append(uname)
        uemail = user['email']
        ue.append(uemail)
    #abc = ['a','b','c']
    #cnt = len(a)
    #return jsonify({'users': users})
    return render_template('users.html', users = users, un = un, ue = ue, cnt = cnt)



    # for a in users:
    #     n = a.name
    #     e = a.email
    #     data1 = {'name' : n}
    #     data2 = {'email' : e}
    #     return render_template('users.html', data1 = {'name' : n}, data2 = {'email' : e})

if __name__ == "__main__":
    app.run(debug=True)
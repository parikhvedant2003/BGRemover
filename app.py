from flask import Flask, request, redirect, render_template
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.secret_key = "parikhvedant2k3"

UPLOAD = r'C:\Users\LENOVO\Desktop\Projects\BGRemover\static'
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), UPLOAD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS_PNG = set(['png'])
ALLOWED_EXTENSIONS_JPG_JPEG = set(['jpg', 'jpeg'])

def allowed_file_png(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PNG)

def allowed_file_jpg_jpeg(filename):
    return ('.' in filename) and (filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_JPG_JPEG)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    file = request.files['image']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file_png(file.filename):
        original_filename = secure_filename(file.filename)
        original_file_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        file.save(original_file_path)
        new_filename = 'BGRemoved.png'
        new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        input = Image.open(original_file_path)
        output = remove(input)
        output.save(new_file_path)
        return render_template('index.html', original_file=original_filename, new_file=new_filename)
    elif file and allowed_file_jpg_jpeg(file.filename):
        original_filename = secure_filename(file.filename)
        original_file_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
        file.save(original_file_path)
        image = Image.open(original_file_path)
        rgb_image = image.convert("RGB")
        png_converter = 'PNGConverted.png'
        png_converter_path = os.path.join(app.config['UPLOAD_FOLDER'], png_converter)
        rgb_image.save(png_converter_path, "PNG")
        new_filename = 'BGRemoved.png'
        new_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        input = Image.open(png_converter_path)
        output = remove(input)
        output.save(new_file_path)
        return render_template('index.html', original_file=original_filename, new_file=new_filename)
    else:
        return redirect(request.url)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
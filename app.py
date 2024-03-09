from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
from io import BytesIO
import os
import cv2
from PIL import Image

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# the folder where we are saving the uploaded files
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# path for static files
app.config['STATIC_FOLDER'] = 'static'



# we are just rendering the upload form
@app.route('/', methods=['GET', 'POST'])
def home():
    data = dict()
    if request.method == 'POST':
        width = request.form['width']
        height = request.form['height']
        size = request.form['size']

        
        if request.files['image-input']:
            print(1)
            file = request.files['image-input']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            filepath = UPLOAD_FOLDER + '/' + filename

            
        else:
            
            filepath = request.form['alter_image_input']


        if width and height:

            width = int(width)
            height = int(height)

            filepath = image_size_adjuster(filepath, width, height)

            data['filepath'] = filepath

        if size:
            size = int(size)

            type_ = request.form['size_type']

            if type_ == 'mb':
                size = size * 1024

            resize_file_size(filepath, filepath, size)

            data['filepath'] = filepath
        
        data['filepath'] = filepath

    return render_template('upload.html', data=data)


def resize_file_size(input_path, output_path, target_size_kb):
   
    # Open the input image file
    with Image.open(input_path) as img:
        # Initialize quality for compression
        quality = 95

        # Loop until the file size is less than the target size
        while True:
            # Save the image with the current quality
            img.save(output_path, quality=quality, optimize=True)

            # Get the size of the saved image file
            file_size_kb = os.stat(output_path).st_size / 1024

            # Check if the file size is within the target size range
            if file_size_kb <= target_size_kb:
                break

            # Decrease the quality for further compression
            quality -= 5
            if quality < 10:
                break


def image_size_adjuster(filename, width, height):

    image = cv2.imread(filename)
    resized_image = cv2.resize(image, dsize=(width, height))

    cv2.imwrite(filename, resized_image)

    return filename






if __name__ == '__main__':
    app.run(debug=True)
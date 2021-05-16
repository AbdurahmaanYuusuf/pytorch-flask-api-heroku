import os
import shutil
import glob
from flask import Flask, render_template, request, redirect

from inference import get_prediction
from commons import format_class_name

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        if not files:
            return
            
        filenames=[]
        for file in glob.glob(UPLOAD_FOLDER+'/*'):
            filenames.append(file)
        results=[]
        for file in glob.glob(UPLOAD_FOLDER+'/*.jpg'):
            class_id, class_name = get_prediction(file)
            class_name = format_class_name(class_name)
            results.append(class_name)
        os.rmdir(UPLOAD_FOLDER)
        return render_template('result.html', results=results,files=filenames)
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))

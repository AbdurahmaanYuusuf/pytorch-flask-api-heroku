import os
import shutil

from flask import Flask, render_template, request, redirect

from inference import get_prediction
from commons import format_class_name

app = Flask(__name__)
    

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return redirect(request.url)
        files_src = request.files.getlist('files[]')
        if not files_src:
            return
        files_dst='/static/uploads'
        files = shutil.copytree(files_src, files_dst, copy_function = shutil.copy)
        filenames=[]
        for file in files:
            file_name=file.filename
            filenames.append(file_name)
        results=[]
        for file in files:
            class_id, class_name = get_prediction(file)
            class_name = format_class_name(class_name)
            results.append(class_name)
        return render_template('result.html', results=results,files=filenames)
    return render_template('index.html')
    


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))

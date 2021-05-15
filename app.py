import os

from flask import Flask, render_template, request, redirect

from inference import get_prediction
from commons import format_class_name

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files.get('file')
        if not file:
            return
        img_bytes = file.read()
        results=[]
        for img_byte in img_bytes:
            class_id, class_name = get_prediction(image_byte=img_byte)
            class_name = format_class_name(class_name)
            results.append(class_name)
        return render_template('result.html', class_name=results)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))

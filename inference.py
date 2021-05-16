import json

from commons import get_model, transform_image

model = get_model()
imagenet_class_index = json.load(open('imagenet_class_index.json'))


def get_prediction(file):
    try:
        input = transform_image(file)
        outputs = model(input)
        for element in outputs:
            index=element.data.numpy().argmax()
        pred=classes[index]
        return pred
    except Exception:
        return 0, 'error'
    #_, y_hat = outputs.max(1)
    #predicted_idx = str(y_hat.item())
    #return imagenet_class_index[predicted_idx]

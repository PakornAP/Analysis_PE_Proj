import yaml
from yaml.loader import SafeLoader

def get_classname():
    with open('static/custom_train_model/dataset/data.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)
    return data["names"]
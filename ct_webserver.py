from ct_main import CT

import threading

from flask import Flask, json, request


def app_factory(config_path, fake):
    app = Flask(__name__)
    ct = CT(config_path, fake)
    thread = threading.Thread(target=ct.run, daemon=True)
    thread.start()

    @app.route('/')
    def hello():
        return 'hello werld'

    @app.route('/press')
    def press():
        def generate():
            yield 'chiming the time...'
            ct.button_press_handler()
            yield 'you pressed the button, bitch'
        return app.response_class(generate())

    @app.route('/save_config', methods=['POST'])
    def save_config():
        old_config = ct.config.as_dict()
        new_config = ct.config.as_dict()
        for k, v in old_config.items():
            t = type(v)
            if t is bool:
                t = lambda x: True if x.lower() == 'true' else False
            new_value = t(request.form.get(k, v))
            new_config[k] = new_value
        ct.config.save_config(new_config)
        return 'config saved'


    @app.route('/load_config')
    def load_config():
        return json.jsonify(ct.config.as_dict())

    return app


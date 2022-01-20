from ct_main import CT

import threading
from datetime import datetime

from flask import Flask, json, render_template, request, send_from_directory


def app_factory(config_path, fake):
    app = Flask(__name__)
    ct = CT(config_path, fake)
    thread = threading.Thread(target=ct.run, daemon=True)
    thread.start()

    @app.route('/')
    def hello():
        return render_template('index.html')

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    @app.route('/chime')
    def chime():
        def generate():
            yield 'chiming the time... '
            ct.button_press_handler()
            yield f'done at {datetime.now()}'
        return app.response_class(generate())

    @app.route('/chime_grandfather')
    def chime_grandfather():
        def generate():
            yield 'grandfather clocking...'
            ct.play_grandfather(datetime.now())
            yield f'done at {datetime.now()}'
        return app.response_class(generate())

    @app.route('/save_config', methods=['POST'])
    def save_config():
        old_config = ct.config.as_dict()
        new_config = ct.config.as_dict()
        for k, v in old_config.items():
            t = type(v)
            if t is bool:
                value = request.form.get(k, None)
                new_value = True if value is not None else False
            else:
                new_value = t(request.form.get(k, v))
            new_config[k] = new_value
        ct.config.save_config(new_config)
        return f'Config saved at {datetime.now()}'


    @app.route('/load_config')
    def load_config():
        return json.jsonify(ct.config.as_dict())

    return app


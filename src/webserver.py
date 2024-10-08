from music import Music

import threading
from datetime import datetime
import logging

from flask import Flask, json, render_template, request, send_from_directory

def app_factory(ct):
    app = Flask(__name__)
    music = Music(ct.play_note)
    thread = threading.Thread(target=ct.run, daemon=True)
    thread.start()

    @app.route('/')
    def hello():
        return render_template('index.html')

    @app.route('/auld')
    def auld():
        def generate():
            yield 'playing a merry tune...'
            music.auld()
            yield 'happy new year!'
        return app.response_class(generate())

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    @app.route('/chime')
    def chime():
        def generate():
            yield 'chiming the time... '
            ct.chime_the_time()
            yield f'done at {datetime.now()}'
        return app.response_class(generate())

    @app.route('/chime_grandfather')
    def chime_grandfather():
        def generate():
            yield 'grandfather clocking...'
            ct.play_grandfather(datetime.now())
            yield f'done at {datetime.now()}'
        return app.response_class(generate())

    @app.route('/chime_test')
    def chime_test():
        def generate():
            yield 'playing all chimes...'
            ct.play_test()
            yield f'done at {datetime.now()}'
        return app.response_class(generate())

    @app.route('/save_config', methods=['POST'])
    def save_config():
        logging.debug(request.form)
        old_config = ct.config.as_dict()
        new_config = ct.config.as_dict()
        for k, v in old_config.items():
            t = type(v)
            if t is bool:
                value = request.form.get(k, None)
                new_value = True if value is not None else False
            else:
                possible_value = request.form.get(k, None)
                if possible_value:
                    new_value = t(possible_value)
                else:
                    new_value = v
            new_config[k] = new_value
        ct.config.save_config(new_config)
        return f'Config saved at {datetime.now()}'

    @app.route('/load_config')
    def load_config():
        return json.jsonify(ct.config.as_dict())

    return app
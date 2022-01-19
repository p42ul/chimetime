from ct_main import CT

import threading

from flask import Flask


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
        t = threading.Thread(target=ct.button_press_handler, daemon=True)
        t.start()
        return 'you pressed the button, bitch'

    return app


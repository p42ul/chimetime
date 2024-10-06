"""The main Chime Time program. Run this at system startup
to run your clock."""
from ct_main import CT
from webserver import app_factory

import argparse
import logging

logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument('--fake', action='store_true', help='If set, will print instead of setting mux outputs.')
args = parser.parse_args()

# This should only be used for testing.
# Use a real WSGI server in production.
if __name__ == '__main__':
    ct = CT('fake') if args.fake else CT('real')
    app = app_factory(ct)
    app.run(host='0.0.0.0', port=5000)
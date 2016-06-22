#!/usr/bin/env python
from fmrapi import app, config

app.run(host='127.0.0.1', port=8088, debug=config.debug)

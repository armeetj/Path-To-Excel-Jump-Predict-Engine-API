import flask;
from flask import Flask;
from api import app;

app.run(host = '0.0.0.0', port = 5000, debug = True)


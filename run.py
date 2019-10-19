from flask import Flask
from templates import app

app.config.from_object('configurations.DevelopmentConfig')
app.run(port="5009")

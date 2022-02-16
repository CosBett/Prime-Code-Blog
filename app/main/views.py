from turtle import title
from flask import render_template, redirect, url_for
from app.main import main

@main.route('/')
def index():
    print('lllllll')
    return render_template('index.html')

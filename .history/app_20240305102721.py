from ensurepip import bootstrap
from operator import index
from flask_bootstrap import Bootstrap
from flask import Flask,render_template, request,jsonify,redirect, session,g, url_for,flash
import logging,json,os
from kiteconnect import KiteConnect
import os
from flask_mysqldb import MySQL
import bcrypt
import mysql.connector
from mysql.connector import Error
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,template_folder='templates',static_folder='static')
if __name__ == '__main__':
     app.run(port=5001,debug=True)
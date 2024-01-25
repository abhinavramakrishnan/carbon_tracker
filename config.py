# taken from previous coursework
import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True
SECRET_KEY = "uIweFg*9wiwOfi.cisShf>IoUe&fh.s1lfJdhfWscaj&esdfi.<edsisdHL"
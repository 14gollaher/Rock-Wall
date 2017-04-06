import os
from flask import Flask, flash, redirect, render_template, request, session, abort
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
from sqlalchemy import text, create_engine
import sqlalchemy 
import sys
import databaseFunctions
import itertools
from itertools import *
import re

class IncidentReport:
    def __init__(self, id, time, date, description, author):
        self.id = id
        self.time = time
        self.date = date
        self.description = description
        self.author = author

def reporting():
    if not session.get('isLoggedIn'):
        return redirect('login')
    return render_template('reporting.html')

def addIncidentRoute():
    currentUserFullName = session.get('currentUserFirstName') + ' ' + session.get('currentUserLastName')
    newIncidentReport = IncidentReport("null", str(request.form['incidentTime']), str(request.form['incidentDate']), str(request.form['incidentDescription']), currentUserFullName)
    databaseFunctions.insertNewIncidentReport(newIncidentReport)
    return redirect('reporting')
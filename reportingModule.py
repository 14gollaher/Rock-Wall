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
    def __init__(self, id, time, date, description, author, isReviewed):
        self.id = id
        self.time = time
        self.date = date
        self.description = description
        self.author = author
        self.isReviewed = isReviewed

def reporting():

    if not session.get('isLoggedIn'):
        return redirect('login')

    if session.get('currentUserAccountType') == 'employee':
        return redirect('reportingEmployee')
    elif session.get('currentUserAccountType') == 'administrator':
        return redirect('reportingAdmin')
    elif session.get('currentUserAccountType') == 'master':
        return redirect('reportingMaster')
    
def reportingEmployee():

    if not session.get('isLoggedIn'):
        return redirect('login')

    return render_template('reporting.html')

def reportingAdmin():

    if not session.get('isLoggedIn'):
        return redirect('login')

    return render_template('reportingManager.html')

def reportingMaster():

    if not session.get('isLoggedIn'):
        return redirect('login')

    reportTable = {}
    reportTable['id'] = databaseFunctions.getAllIncidentReportIds()
    reportTable['time'] = databaseFunctions.getAllIncidentReportTimes()
    reportTable['date'] = databaseFunctions.getAllIncidentReportDates()
    reportTable['description'] = databaseFunctions.getAllIncidentReportDescriptions()
    reportTable['author'] = databaseFunctions.getAllIncidentReportAuthors()
    reportTable['isReviewed'] = databaseFunctions.getAllIncidentReportIsRevieweds()
    reportTable = [dict(id=i, time=t, date=d, description=de, author=a, isReviewed=ir) for i, t, d, de, a, ir in zip(reportTable['id'], reportTable['time'], reportTable['date'], reportTable['description'], reportTable['author'], reportTable['isReviewed'])]
    
    return render_template('reportingManager.html', reportTable = reportTable)

def addIncidentRoute():

    if not session.get('isLoggedIn'):
        return redirect('login')

    currentUserFullName = session.get('currentUserFirstName') + ' ' + session.get('currentUserLastName')
    newIncidentReport = IncidentReport("null", str(request.form['incidentTime']), str(request.form['incidentDate']), str(request.form['incidentDescription']), currentUserFullName, "No")
    databaseFunctions.insertNewIncidentReport(newIncidentReport)
    return redirect('reporting')


def toggleReportReviewStatus():

    if not session.get('isLoggedIn'):
        return redirect('login')

    if str(request.form['isReviewed']) == 'Yes':
        incidentReport = IncidentReport(str(request.form['id']), "", "", "", "", "No" )
    else:
        incidentReport = IncidentReport(str(request.form['id']), "", "", "", "", "Yes" )
       
    databaseFunctions.toggleIncidentReportIsReviewed(incidentReport)
    return redirect('reporting')


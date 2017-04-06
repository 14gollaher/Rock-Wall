import os
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask import make_response
from sqlalchemy.orm import sessionmaker, scoped_session
import datetime
from sqlalchemy import text, create_engine
import sqlalchemy 
import sys
import databaseFunctions
import simplejson as json

class CalendarItem:
    def __init__(self, id, title, startTime, description, icon, color):
        self.id = id
        self.title = title
        self.startTime = startTime
        self.description = description
        self.icon = icon
        self.color = color

def calendar():
    if not session.get('isLoggedIn'):
        return redirect('login')

    calendarIds = databaseFunctions.getAllCalendarIds()
    calendarTitles = databaseFunctions.getAllCalendarTitles()
    calendarStartTimes = databaseFunctions.getAllCalendarStartTimes()
    calendarDescriptions = databaseFunctions.getAllCalendarDescriptions()
    calendarIcons = databaseFunctions.getAllCalendarIcons()
    calendarColors = databaseFunctions.getAllCalendarColors()

    calendarIds = json.dumps(calendarIds)
    calendarTitles = json.dumps(calendarTitles)
    calendarStartTimes = json.dumps(calendarStartTimes)
    calendarDescriptions = json.dumps(calendarDescriptions)
    calendarIcons = json.dumps(calendarIcons)
    calendarColors = json.dumps(calendarColors)

    return render_template('calendar.html', calendarIds = calendarIds, calendarTitles = calendarTitles, calendarStartTimes = calendarStartTimes, calendarDescriptions = calendarDescriptions, calendarIcons = calendarIcons, calendarColors = calendarColors)

def calendarUpdate():
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        startTime = request.form['startTime']
        description = request.form['description']
        if description == "-1Nullx0":
            description = None
        icon = request.form['icon']
        color = request.form['color']
        newCalendarItem = CalendarItem(id, title, startTime, description, icon, color)
        if databaseFunctions.getCalendarItemId(newCalendarItem):
            databaseFunctions.changeCalendarItemStartTime(newCalendarItem, newCalendarItem.startTime)
        else:
            if id != '_fc1':
                databaseFunctions.insertNewCalendarItem(newCalendarItem)
    return redirect('calendar')

def calendarInsert():
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['title']
        startTime = request.form['startTime']
        description = request.form['description']
        if description == "-1Nullx0":
            description = None
        icon = request.form['icon']
        color = request.form['color']
        newCalendarItem = CalendarItem(id, title, startTime, description, icon, color)

        databaseFunctions.insertNewCalendarItem(newCalendarItem)

    return redirect('calendar')

def calendarDelete():
    if request.method == 'POST':
        id = request.form['id']
        newCalendarItem = CalendarItem(id, "", "", "", "", "")
        databaseFunctions.deleteCalendarItem(newCalendarItem)
    return redirect('calendar')

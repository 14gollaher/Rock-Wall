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

class Message:
    def __init__(self, id, author, time, content):
        self.id = id
        self.author = author
        self.time = time
        self.content = content

def message():
    if not session.get('isLoggedIn'):
        return redirect('login')

    messageTable = {}
    messageTable['author'] = databaseFunctions.getTop100MessageAuthors()
    messageTable['time'] = databaseFunctions.getTop100MessageTimes()
    messageTable['content'] = databaseFunctions.getTop100MessageContents()
    messageTable = [dict(author=a, time=t, content=c) for a, t, c in zip(messageTable['author'], messageTable['time'], messageTable['content'])]
    return render_template("message.html", messageTable = messageTable)

def addMessage():
    currentUserFullName = session.get('currentUserFirstName') + ' ' + session.get('currentUserLastName')
    newMessage = Message('-1Nullx0', str(currentUserFullName), str(datetime.now().strftime('%b-%d %I:%M %p')), str(request.form['content']))
    newMessage.content = '\n' + newMessage.content
    databaseFunctions.insertNewMessage(newMessage)
    return redirect('message')
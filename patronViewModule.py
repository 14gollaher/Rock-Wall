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

def patronViewEmployee():
    
    patronTable = {}
    patronTable['id'] = databaseFunctions.getAllPatronIds()
    patronTable['firstName'] = databaseFunctions.getAllPatronFirstNames()
    patronTable['lastName'] = databaseFunctions.getAllPatronLastNames()
    patronTable['isBelayCertified'] = databaseFunctions.getAllPatronBelayCertifications()
    patronTable['isSoloClimbCertified'] = databaseFunctions.getAllPatronSoloClimbCertifications()
    patronTable = [dict(id=i, firstName=f, lastName=l, isBelayCertified = b, isSoloClimbCertified = s) for i, f, l, b, s in zip(patronTable['id'], patronTable['firstName'], patronTable['lastName'], patronTable['isBelayCertified'], patronTable['isSoloClimbCertified'])]
    
    return render_template('patronViewEmployee.html', patronTable = patronTable)
<h3>
Web application for South Dakota State University - Junior Software Engineering Course.
</h3>

<h4>
Developed by: Matthew Gollaher, Kyle Paxton, and Abu Daud Talukder
</h4>

The application was built for the University Wellness Center Climbing Wall. The application features login, inventory management, patron management, user management, chat, calendar and reservations, a patron tablet signature usage. The web application not only fulfilled the requirements, but was the winning and chosen project across three different Junior, Senior, and Graduate level software engineering classes - all implementing this project. The application uses the following:

Python
Flask
HTML
Bootstrap
CSS
Javascript
jQuery

This project was my head-first introduction into one of my favorite things today, web development. There are numerous things I'd do differently with this project if I was starting over, and there are numerous problems and room for refactoring within this application. While it's on my to-do list to refactor some of this project, it's fun to look back at something I developed only months ago and say "wow, I could have done a much better job with this." 

Below are instructions to utilize this application. The example urls given are www.matthewgollaher.com where I am as of time writing this, hosting the web application. Feel free to break this of course! If yuo're just perusing, you can skip to to #6 in DESKTOP ENVIRONMENT and #3 in TABLET ENVIRONMENT

<hr/>

The system includes two independent environments, one desktop environment and one tablet environment. An online
URL is provided for convenience of demonstration purposes, but it should be noted that Internet is NOT necessary
to use the application in production. 

While the application is accessible (but not tested) on other operating systems than Windows, these instructions only
walktrough the database backup process on a Windows 10 OS - though the instructions will be similar, if not identical,
to a Windows 7 or 8 OS.


DESKTOP ENVIRONMENT: 

1. The desktop system must be used in Chrome, as other browsers do not have support for some features of the system and some
   elements are not optimzed for other browsers. The system was tested for release with Chrome version 57.0.2987.133.

2. Touch events must be turned off for many features of this system. To do this:
	a) In Chrome, enter the following URL into the search bar: "chrome://flags"
	b) Turn Touch Events API to Disabled.

3. Adobe Flash must be turned on. To do this:
	a) In Chrome, enter the following URL into the search bar: "chrome://settings/content"
	b) In the "Flash" section, allow the page to run Adobe Flash by either selecting "Allow sites to run Flash" or adding an exception.

4. As the system is used by multiple users, incognito or private browsing is suggested to avoid caching and security issues between users. 
	a) To active private browsing, click "CTRL + SHIFT + N" within Chrome to open a new
           private browing window. 

5. The system is best viewed in full screen mode. Failure to utilize full screen mode may result incorrectly rendered browser content.
        a) To activate full-screen mode, from Chrome click "F11".

6. To access the desktop system, proceed to given URL "www.matthewgollaher.com"

7. There are 3 tiers of access - Employee, Master, and Administration. Three different accounts are setup for the system demonstration:
	a) Employee:
	    - USERNAME: e@gmail.com
	    - PASSWORD: abc123
	b) Administrator:
	    - USERNAME: a@gmail.com
            - PASSWORD: abc123
        c) Master:
	    - USERNAME: m@gmail.com
            - PASSWORD: abc123

8. The desktop system is now fully accessible.

TABLET ENVIRONMENT: 

1. The tablet system must be used in Chrome, as other browsers do not have support for some features of the system and some elements are 
   not optimzed for other browsers. The system is not guaranteed, but is intended to work for most standard tablets. The system
   was tested with a Samsung Galaxy Tab S2 tablet using Chrome version 57.0.2987.133.

2. As the system is used by multiple patrons, incognito or private browsing is suggested to avoid caching and security issues between patrons.
	a) Activate private browsing within your mobile browser application's settings.

3. To access the patron's tablet system, proceed to the patron URL on a supported tablet: "www.matthewgollaher.com/patronCheckIn."

4. It is suggested to first create a patron account to be best exercise the patron functionalities. 

5. The desktop system is now fully accessible.


BACKING UP THE DATABASE:

1) 7-Zip must be installed to backup the database.
	a) Download and install from here: http://www.7-zip.org/download.html

1) Locate the DatabseBackup.bat file found in "SDSU Rock Wall\"

2) Right click DatabseBackup.bat and open with a preferred text editor.

3) Change the file path found in line 8 (Or see comment within the file) to the preferred backup location.
	a) Ex: "C:\Users\mattg\Documents\Database Backups"

4) Save and close the text editor.


MANUAL BACKUP: 

1) Simply double click the batch file to execute it. The backed up file will be zipped and accessible in the specified backup location.

AUTOMATIC BACKUP:

1) Open Windows Task Scheduler

2) Click Action -> Create Basic Task

3) Give the task a name and description if desired
	a) EX: "Backup Database"

4) Click "Next"

5) Specify the backup interval you'd like the backup to happen (NOTE: Do not specify more than once a day).
	a) Ex: "Weekly on Monday at 2:30 AM"

6) Click "Next"

7) Select "Start a program" if it is not already selected

8) Click "Next"

9) Specify the batch file directory location from the previous steps
	a) EX: "C:\Users\mattg\Documents\Development Projects\Rock-Wall-SDSU\SDSU Rock Wall\DatabaseBackup.dat"

10) Click "Next"

11) Review the details and click "Finish." The database will now automatically back up to the specified file location on the interval specified. 

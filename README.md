# Spreadsheet Web App

A spreadsheet web application powered by python

[instance running on my home server (will often be down)](http://67.160.178.216/cgi-bin/test.py)

## Features

- cloud storage of spreadsheets
- password protected login
- formulas are writen in python

## Structure

- Using apache, the *cgi* python script is called upon page request.
- The *cgi* script communicates with the *service* python script via fifo.
- The *service* script is continuously run in the background as a linux daemon, this allows for faster response when working with large spreadsheets.
- The *service* script sends infomation about a particular spreadsheet to the *cgi* script.
- The *cgi* script then renders the information as an html page and sends it to the client computer.



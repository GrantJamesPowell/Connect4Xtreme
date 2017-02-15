# Connect4Xtreme
A Django Implementation of the kids game 'Connect Four'

![Alt text](/samplepics/maingame.png?raw=true "Game Screen")
![Alt text](/samplepics/homescreen.png?raw=true "Home Screen")

##Problem Statement: 

Create a web application in the language/framework of your choice that plays the game "Connect Four” interactively (Human vs Computer). 

## What is the difference between "Normal" mode and "X-Treme"?

Normal mode AI can only see one move ahead and tends to only block and play random numbers
X-Treme mode can see much farther ahead and I have yet to be able to beat it

## Why do I need to make an account?

The app saves all your games to a database, so that you can login from anywhere and continue your games

## What outside libraries are used?

All of the logic and web app parts come from the Python 3 standard library and Django Framework

Some Creative Commons CSS templates from html5up.com are used in the front end. Some of the styling css styling
(but not functionality) was inspired by this code-pen example https://codepen.io/coderontheroad/pen/GdxEo

##  Interesting Files

*AI functions:*  
/ConnectFourApp/alphaconnectfour.py  
Has all the computer move functions

*GameBoard Objects:*  
/ConnectFourApp/models.py  
Contains the `GameBoard` class which contains the game logic and database functions

*Ajax endpoint*  
/ConnectFourApp/views.py  
The function (gamedata) contains the ajax get and post methods  

*Game Board Javascript*  
/ConnectFourApp/templates/exts/game_view.html  
The front end javascript

*Tests*
/ConnectFourApp/tests.py
Comprehensive unit test suite

## A little about me!

My name is Grant Powell, I'm a software engineer out of the University of Tennessee. I worked at Oak Ridge National Laboratory in the summer of 2015 in the Computational Science and Engineering Division. While at Oak Ridge I wrote software as part of the Department of Energy's
Smart Snow Removal Project that speed up processing from 132 hours to less than 3 for the city of Knoxville. Last summer,  I was a software engineering intern in the FedEx Technical Architecture Division. My FedEx intern team and I became the first ever win the highest intern award twice in a row. 

My passion is building software that helps people. I’m on the executive board of my fraternity, and while on the board I built an attendance web app that keeps track of attendance through QR scans on snapchat. The attendance system has been used at over 50 events with over 2000 sign-ins and is well received by brothers. I’m looking forward in my career to building more awesome software that helps people accomplish their goals.

![Alt text](/ConnectFourApp/static/assets/images/connect4.gif?raw=true "Game Screen")


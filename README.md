# project
## CS50 Final Project
## Nocturnal Meditations Blog Website
### Motivation and Context
  Welcome to my CS50 final project. The end state goal for this project is a website hosted on either Azure, AWS, or google cloud where I can post essays about different topics and then meta essays trying to connect the different essays togather as a way of making sense of the world and connecting the dots of what is really going on. I do not intend to submit the goal of what I really want this blog to be in fact as of doing this final project I have not fully finished any of the essays I want to feature. The goal is that this will be a life long hobby of making this web app/site the best it can be and just really being I a place I can get my thoughts out there in anynous way. I plan on changing the name of the blog as well after submitting as I like the idea of haveing an anynomous blog in the sytle of the zerohedge twitter handle and many others who do similar things. 

  This is my second attempt at the final project. My first attempt at the final project was a scheduling web app using flask and SQL lite. The goal was a simple to use web app where Air Force flying squadrons could quickly build, edit, and diseminate monthly, weekly, and daily flying schedules while being able to track all flight records of individual pilots within the squadron. After putting about 15 hours into that project I decided to go somewhere else, but that said I'm still proud of how it went I was able to create a complictated SQLite database tha actually worked for pulling sorties and saving record too. However, to actually make the front end anything near what I wanted, and thus influence thus actually create usability for pilots I have a very long way to go and it was me biting off more than I can chew at this time. 

  I created my own github account and coded the entirity of this project in a github codespace so I could learn how to use github, flask, and SQLite3 without the CS50 training wheels provided in the CS50 IDE, which is something I saw as crutial if I am to one day be a competent software engineer. To that end I would say this final project has been a great success and I have learned a tremendous amount about the IOT side of the programming world and how real life applications and solutions are collaboritvly worked on, though this project was just me, and how they are deployed as well. I now have a real appreciation for how difficult the deployment side of things can be.

  Additionally I can say that while this blog is simple and getting the navbar to actually function took time I have now probable spent triple the amount of time trying to figure out how to host my website on AWS/Azure/Heroku/github pages than on actually creating my web app and the process has been incredibly frustrating. I would like to say thank you to the Harvard CS50 team this course has been incredible and I have enjoyed it alot. I would only ask that there be an additonal extra week where you simply step through how wo host a web app on a cloud service,that said I am fully aware that is not the purpose of the class so again I say THANK YOU!!!

## Implementation for Nocturnal Mediations Flask & Bootsrtap Based Web App:
  This blog website will be a flask based web app using the bootstrap frame work. Additionally I will trying to implement a SQLite database to create a list of "subscribers" to get emails for theoretical news letter that will come later on down the road and being as when I submit this project I won't have any will be an empty database but the framework will be there. 
  I tried to structure this as well as I could. The structure being inside the main project folder there is the __pycache_ to allow python implementation of flask. a flask session to hold "cookies" about who is currently using the site if a person decides to sign up as a "subscriber". Then I have a static folder containing my stylesheet, then another folder inside the static which contains images, of note all images were created by myself using midjourney, then another folder inside static called templated containing all the .html files my web app uses. Then back to simpl insisde the priject folder my app.py, LISENCE, project.db a SQLite3 database with the highlight I used the graphical extention available inside VS studios to make working with the database far more intuitive, and finaly the README file.
Description below
Project Folder
  pycache
  flask_session
  static
    css
      style.css
    images
      ...
    templates
      .html ...
  app.py
  LICENSE
  project.db
  README

### Layout.html
My layout.html file serves as the skeleton for all of my web app's html pages to serve a consistent vanbar and footer as well as handle all the admin of pulling in the required links needed to have a polished bootstrap library. It employs jinja as well to be able to change content based on what page of the web app the user is currently using. 
  The first section of the layout.html file after puuling in all needed libraries for a bootstrap based web app is the header section wichi serves to create a consistant and elegant title block across all web pages. In the header I chose to include the "login" and "subscribe" links so that a user would see them at the top of the page every time.
    The next section in the layout.html file is my navbar section. It is a pretty typical bootstrap style navbar. On the left hand side is the standard bootstrap navbar button to show the navbar in case the user is viewing on a small screen and window and the viewport would cut off the majority of the navbar. Next I have a standard nav-item which is a link to index.html which is simply called home so no matter what web page the user finds themself on they can simply return to the main page of the web app. Next I have a navbar drop down where the user can use a drop down to access all essays on the web app. With the highlight that I intend to actually write more and add more so this drop down would implement all the essays not currently available on the navbar. Next I simply have the nav-links to the pages of each essay, these would be the most recent left to right, then again the idea with the drop down is once there are too many essays to have on the navbar they are placed in the drop down. After the essays I have a very simply jinja based nav-item to simply show the user_name of the "subscriber" who is currently logged in, and finally on the navbar I have the log out which calls the logout function in my app.py file. 
      The next two sections in the layout.html file are a simple place holder for a jinja body block to be added by other .html files and then a very simple footer section that will be maintained across all web pages.

### app.py
  The app.py file is the heart and brain of my flask based web app if layout.html is the skeleton. Some things you find throughout are week 9 hold overs and some additional extra code to use SQLite3 without the use of the CS50 training wheels. 
    Like any app.py file it starts


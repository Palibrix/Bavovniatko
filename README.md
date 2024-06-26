
# 🚀 Bavovniatko 🔥
[![Me][user-badge]][user-url]

----

[![Python][python-badge]][python-url]

[![Docker][docker-badge]][docker-url]
[![PyCharm][pycharm-badge]][pycharm-url]
[![DjangoREST][django-rest-badge]][django-url]
[![Postgres][postgres-badge]][postgres-url]

[![GitHub issues][git-issues]][git-issues-url]
[![GitHub branches][git-branches]][git-url]
![GitHub last-commit][git-last-commit]
[![GitHub Maintenance][git-maintenance]][git-activity-url]
----
## 📝 Table of Contents
1. [🔍 What is this repository about?](#-what-is-this-repository-about)
2. [❓ Why?](#-why)
3. [💻 Installing](#-installing)
4. [🛠 Technologies](#-technologies)
5. [👤 User story](#-user-story)
____

## 🔍 What is this repository about?
Welcome, dear stranger, on a journey to the skies with Bavovniatko.

> You might ask yourself a question: “What does this name means?”. Well, The term “бавовна” (bavovna), which literally means “cotton” in Ukrainian, became an internet meme and symbol during the russian invasion of Ukraine. It humorously refers to explosions, both in Russian-occupied Ukraine and in Russia itself. The word is a mistranslation of the Russian “хлопок”(crack, snap, pop, a euphemism for an explosion), that also means “cotton” in Russian and was incorrectly translated by automated translation tools.

Let's get back to the point. This project is all about building your FPV drones. 
But the most important feature — it helps to pick right parts and providing complete and detail information about them.  

## 🤔 Why?
FPV drones have revolutionized the way warfare is conducted, serving as the eyes and arms of soldiers. While some may not consider it, drones could become a form of rehabilitation for many individuals after the war. Additionally, FPV drones have also found their place as a popular hobby, with tournaments being held for enthusiasts.

Selecting the right parts for building FPV drones can be quite challenging due to the various parameters to consider, such as fittings, types of antennas, batteries, and more. It's easy to become overwhelmed if you're new to this. You might end up spending a lot of money on parts, only to find out that they are not compatible with each other. Even if you are knowledgeable about drones, the sheer variety of available parts with unique properties can be daunting. Furthermore, different websites may provide conflicting specifications for the same model.

> The goal of the project is to help individuals find parts with confirmed specifications through documentation or testing.


## 🐒 Installing
Nothing here (yet)

## 🛠 Technologies
* Python
* My own markdown library (yet to be published)
* Django
* DRF
* PostgreSQL
* To be continued...

# 👤 User story
____


<details>
<summary>

## V1
### Base version, simple operations

</summary>

## `Anonymous`
1. As an `Anonymous`, I can view all official Parts, that is I can search across the site or get data via open API
2. As an `Anonymous`, I can view any detailed information of any official Part, that is I can either send a request via API or open information about Part on website
3. As an `Anonymous`, I can search and filter official Parts
4. As an `Anonymous`, I can view any official drone, that is I can view only drones, that are made of official Parts and were selected by administrators

----
## `User`
1. As a `User`, I can do everything `Anonymous` does 
2. As a `User`, I can login, so that I can use all functionality of website
3. As a `User`, I can logout
4. As a `User`, I can register new account
5. As a `User`, I can create any drone Part, that I can add to my own Drone
6. As a `User`, I can not create Part, that is a copy of my own Part or official Part
7. As a `User`, I can create Drone from either official, unofficial or my own Parts, that is I can name it and select any Parts
8. As a `User`, I can view, search and filter Parts on a Drone creation page, that is I can easily find what I was looking for. Official Parts will be included first
9. As a `User`, I can see warnings if Part is not official and/or not fully completed
10. As a `User`, I can drag-and-drop Part when creating Drone, that is I can pick Part from a list and drop it onto build
11. As a `User`, I can get a more detailed information about Part, when I hover over it on Drone creation page 
12. As a `User`, I can update any of my drone Parts
13. As a `User`, I can delete any of my drone Parts
14. As a `User`, I can view any Part, so that I could filter official and unofficial and see warnings if viewed Part is not official
15. As a `User`, I can view any Drone, so that I could filter official and unofficial and see warnings if viewed Drone is not official
16. As a `User`, I can search for a Part, that is I can search something in a specific category (e.g. engine, batteries) by model and manufacturer
17. As a `User`, I can filter Parts, that is I can filter Part in a specific category by manufacturer or Part-specific values
18. As a `User`, I can search for a Drone, that is I can search something in a specific category (sport, photography) by name
19. As a `User`, I can filter Parts, that is I can filter Drone in a specific category by Drones Part-specific values

---- 
## `Administrator`
1. As an `Administrator`, I can do everything `User` does 
2. As an `Administrator`, I can use Django admin website do manage database
3. As an `Administrator`, I can update any Part, that is I can make Part public
4. As an `Administrator`, I can delete any Part
5. As an `Administrator`, I can update any Drone, that is I can make drone public
6. As an `Administrator`, I can delete any Drone
7. As an `Administrator`, I can update any `User`
8. As an `Administrator`, I can delete any `User`

</details>


<details>
<summary>

## V2
### Making Parts or drones public

</summary>

## `Anonymous`
1. As an `Anonymous`, I can do everything I could do in a V1

----
## `User`
1. As a `User`, I can do everything I could do in a V1 
2. As a `User`, I can make a publicity request for a Part or a build, that is admin would review my Part or build and make it public if everything is correct, so that my Part will become official
3. As a `User`, I can add a comment to the publicity request, so that reviewer will get some information on where or how he can confirm Part characteristics
4. As a `User`, I can add a file to publicity request, that is I can add documentation
5. As a `User`, I can receive points for my profile, that is I can get new statuses or badges
6. As a `User`, I can see other people statuses or badges, that is near their name everywhere
7. As a `User`, I can send a change request for any official Part, that is I can specify what exactly needs to be changed and why
8. As a `User`, I can add a file to my change request, that is I can proof myself correct
9. As a `User`, I can view all pending change requests, so that I won't send same request
10. As a `User`, I can not longer update or delete item after it became public, even if I created it

---- 
## `Administrator`
1. As an `Administrator`, I can do everything I could do in a V1
2. As an `Administrator`, I can accept or deny publicity requests, that is Part's or build's publicity will be changed automatically
3. As an `Administrator`, I can accept or deny change request


</details>


<details>
<summary>

## V3
### Parts compatibility checker

</summary>

## `Anonymous`
1. As an `Anonymous`, I can do everything I could do in a V2
2. As an `Anonymous`, I can read featured guides about FPV Parts

----
## `User`
1. As a `User`, I can do everything I could do in a V2
2. As a `User`, I can see list of drones, that was made of specific Part, that I am looking at, so that whenever I read detailed information, I can see list of official Drones 
3. As a `User`, I can check Parts compatibility in my Drone, so that I can press a button and receive list of all incompatibilities
4. As a `User`, I can get system notifications/errors if Parts are not compatible, so that even if I am looking at not my Drone I can see if it built correctly
5. As a `User`, I can see system notifications in real time if Parts are not compatible together in my Build
6. As a `User`, I can receive recommendations for some parts, if I system meets minimum requirements

---- 
## `Administrator`
1. As an `Administrator`, I can do everything I could do in a V2


</details>


<details>
<summary>

## V4
### Social Part
[//]: # (Comments for official Parts, create account with socials, user actions;)

[//]: # (add ability users to report Parts for inapropraite names etc.)

[//]: # (New role - Manager (from Admin}, that can edit only Parts and Drones)

</summary>

## `Anonymous`
1. As an `Anonymous`, I can do everything I could do in a V3

----
## `User`
1. As a `User`, I can do everything I could do in a V3
2. As a `User`, I will automatically create Actions, that is system will write down anything I do on the website: GET, POST, PUT, PATCH, DELETE
3. As a `User`, I can I can view details of deleted Part of a Drone that I used in my Build, that is after author deleted part I can view its last data from Actions
4. As a `User`, I can comment any Part or Drone, that is I can comment official and unofficial Parts
5. As a `User`, I can view all comments to any Part or Drone
6. As a `User`, I can delete my comment on any Part or Drone, that is other users will see that comment was deleted
7. As a `User`, I can change my comment on any Part or Drone, that is other users will see changes and that message was edited
8. As a `User`, I can report any `User` comment, that is I can select why I am reporting it or write short note to get `User` banned
9. As a `User`, I can report any `User` Part or Drone
10. As a `User`, I can reply to any `User` comment, so that I can create discussion
11. As a `User`, I can rate a Part or Drone, that is I can rank it from 1 to 5
12. As a `User`, I can view Part or Drone rankings
13. As a `User`, I can sort Part or Drone by ranking, that is while I'm searching for a Part or Drone I can sort and view most popular choices
14. As a `User`, I can view number of votes
15. As a `User`, I can vote for change requests, that is if I think that it is correct change, I can give my upvote for admins for easier and quicker change

----
## `Manager`
1. As a `Manager`, I can

[//]: # (1. As a `Manager`, I can do everything that `Administrator` does, except managing Users, that is I can manage any Part, Drone, Request etc., but can't change User's password or any other data)

---- 
## `Administrator`
1. As an `Administrator`, I can do everything I could do in a V3
2. As an `Administrator`, I can view any user Actions



</details>


<details>
<summary>

## V5
### Lists of parts
[//]: # (Lists of favorites, some kind of named lists to save and group Parts)

</summary>

## `Anonymous`
1. As an `Anonymous`, I can do everything I could do in a V3

----
## `User`
1. As a `User`, I can do everything I could do in a V3


----
## `Manager`
1. As a `Manager`, I can 

---- 
## `Administrator`
1. As an `Administrator`, I can do everything I could do in a V3
2. 



</details>

[user-badge]: https://img.shields.io/badge/Palibrix-DD9623?style=plastic
[user-url]: https://github.com/Palibrix

[django-rest-badge]: https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray
[django-url]: https://www.djangoproject.com/
[docker-badge]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white
[docker-url]: https://docker.com/
[postgres-badge]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[postgres-url]: https://www.postgresql.org/
[pycharm-badge]: https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green
[pycharm-url]: https://www.jetbrains.com/pycharm/
[python-badge]: http://ForTheBadge.com/images/badges/made-with-python.svg
[python-url]: https://www.python.org/

[git-activity-url]: https://GitHub.com/Palibrix/Bavovniatko/graphs/commit-activity
[git-branches]: https://badgen.net/github/branches/Palibrix/Bavovniatko
[git-issues-url]: https://github.com/Palibrix/Bavovniatko/
[git-issues]: https://img.shields.io/github/issues/Palibrix/Bavovniatko
[git-last-commit]: https://img.shields.io/github/last-commit/Palibrix/Bavovniatko
[git-maintenance]: https://img.shields.io/badge/Maintained%3F-yes-green.svg
[git-url]: https://github.com/Palibrix/Bavovniatko/
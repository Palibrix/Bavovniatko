
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
5. [Features](#what-you-can-do)
6. [👤 User story](#-user-story)
____

## 🔍 What is this repository about?
Welcome, dear stranger, on a journey to the skies with Bavovniatko.

> You might ask yourself a question: “What does this name mean?” Well, The term “бавовна” (bavovna), which literally means “cotton” in Ukrainian, became an internet meme and symbol during the russian invasion of Ukraine. It humorously refers to explosions, both in russian-occupied Ukraine and in russia itself. The word is a mistranslation of the russian “хлопок”(crack, snap, pop, a euphemism for an explosion), that also means “cotton” in Russian and was incorrectly translated by automated translation tools.

Let us get back to the point.
This project is all about building your FPV drones. 
But the most important feature –
it helps to pick the right parts and provide complete and detail information about them.  

## 🤔 Why?
FPV drones have revolutionized the way warfare is conducted, serving as the eyes and arms of soldiers. While some may not consider it, drones could become a form of rehabilitation for many individuals after the war. Additionally, FPV drones have also found their place as a popular hobby, with tournaments being held for enthusiasts.

Selecting the right parts for building FPV drones can be quite challenging due to the various parameters to consider,
such as fittings, types of antennas, batteries, and more.
It is easy to become overwhelmed if you're new to this.
You might end up spending a lot of money on parts, only to find out that they aren't compatible with each other.
Even if you're knowledgeable about drones, the sheer variety of available parts with unique properties can be daunting.
Furthermore, different websites may provide conflicting specifications for the same model.

> The goal of the project is to help individuals find parts with confirmed specifications through documentation or testing.


## 🐒 Installing
Nothing here (yet)

## 🛠 Technologies
* Python
* My own Markdown library (PyMarkEditor)
* Django
* DRF
* PostgreSQL
* To be continued...

## What you can do:
1. [ ] Base: view all available parts and drones
2. [ ] Search: search any item 
3. [ ] Filter: filter any Part or Drone by item-specific values
4. [ ] Suggest: suggest parts to add them to the database
5. [ ] Save: select parts and drones for ease access in the future. You also can create item groups (like music playlists)
6. [ ] Create: create drones from parts and see if parts are compatible with each other
7. [ ] Review: comment any Part or Drone
8. [ ] Compare: compare parts of the same type: motors, frames, and so on
9. [ ] Chat: ask specific questions about any part or answer them
10. [ ] Share: share drones you built. You also can share videos with drones you built

| Version     | №  | Features |
|:------------|:--:|:--------:|
| Base        | v1 | 1, 2, 3  |
| Suggestions | v2 |   4, 5   |
| Creations   | v3 |    6     |
| Social      | v4 |   7, 8   |
| Social 2    | v5 |  9, 10   |


# 👤 User story
____


<details>
<summary>

## V1
### Base version, simple operations

</summary>

## `Anonymous`

1. As an `Anonymous`, I can use public API or website to retrieve detailed information about any Part or Drone in the database
2. As an `Anonymous`, I can use public API or website to retrieve a list of Parts or Drones in the database
3. As an `Anonymous`, I can use public API or website to retrieve a list of Parts or Drones in the database, filtered by category or category-specific values
4. As an `Anonymous`, I can use public API or website to search for Part or Drone and retrieve a list of results

## `Administrator`

1. As an `Administrator`, I can do everything `Anonymous` does
2. As an `Administrator`, I can use Django admin website do manage database
3. As an `Administrator`, I can CRUD any Part
4. As an `Administrator`, I can CRUD any Drone

</details>


<details>
<summary>

## V2
### Users, requests, favorites

</summary>

## `Anonymous`
1. As an `Anonymous`, I can do everything I could do in a V1

2. As an `Anonymous`, I can create my account using email, username, password, name, and surname
3. As an `Anonymous`, I can log in into my account using username and password 

## `User`
1. As a `User`, I can log out
2. As a `User`, I can make **Suggestion request** for any type of Part to add into the database
3. As a `User`, I can add commentary and files to my **Suggestion request**
4. As a `User`, I can view all my **Suggestion request** and their statuses (_pending_, _denied_, _approved_) on a separate page
5. As a `User`, I can view commentary to the _status_ if it exists, that is if `Administrator` denied it, I can see the reason
6. As a `User`, I can edit any of my unapproved **Suggestion request**
7. As a `User`, I can reopen any of my _denied_ **Suggestion request** with updated information
8. As a `User`, I can delete any of my **Suggestion request**, regardless of _status_
9. As a `User`, I can make **Change request** to any part that is if you spot a mistake or information is not completed

10. As a `User`, I can add Part to the list of favorites. This list will be displayed as `Favorite`, will be default for each `User` and couldn't be deleted or renamed by me
11. As a `User`, I can create **Part list** with any name to contain any Parts
12. As a `User`, I can edit or delete **Part list**, created by me
13. As a `User`, I can view any of my **Part list**
14. As a `User`, I can add Parts to any of my **Part list**
15. As a `User`, I can remove any Part from any of my **Part list**

## `Administrator`
1. As an `Administrator`, I can do everything I could do in a V1

2. As an `Administrator`, I can do everything `User` does
3. As an `Administrator`, I can CRUD any `User`
4. As an `Administrator`, I can CRUD any **Suggestion request**
5. As an `Administrator`, I can CRUD any **Part list**
6. As an `Administrator`, I can view all **Suggestion request**
7. As an `Administrator`, I can accept **Suggestion request**, so that Part will be added to the database
8. As an `Administrator`, I can deny **Suggestion request**, that is Part won't be added to the database and `User`, who sent the request, will be notified and view the reason
9. As an `Administrator`, I can view all **Change request** and change Part if necessary

</details>


<details>
<summary>

## V3
### Create your own drones

</summary>

## `Anonymous`
1. As an `Anonymous`, I can do everything I could do in a V2

## `User`
1. As a `User`, I can do everything I could do in a V2

2. As a `User`, I can view other people's profiles and _public_ drones they created
3. As a `User`, I can read _public_ drones from people's profiles
4. As a `User`, I can any Drone on the website
5. As a `User`, I can get the list of all my liked Drones
6. As a `User`, I can remove like from any Drone on the website

7. As a `User`, I can view all _public_ Drones created by any `User`
8. As a `User`, I can read any _public_ Drone created any `User`
9. As a `User`, I can filter all _public_ Drones by specifications
10. As a `User`, I can filter all _public_ Drones by completion
11. As a `User`, I can create a new drone with any available Parts. Those drones are _private_ by default. Might not be completed completely
12. As a `User`, I can change visibility of my Drone to _public_ or _private_
13. As a `User`, I can get a warning if Parts aren't compatible with each other. This warning can be disabled. 
Users might send **False error** request with detailed information. Not compatible parts will be displayed with a yellow error triangle
14. As a `User`, I can see a notification if Drone is not completed by any number of Parts
15. As a `User`, I can edit my Drone
16. As a `User`, I can delete my Drone

## `Administrator`
1. As an `Administrator`, I can do everything I could do in a V2
2. As an `Administrator`, I can CRUD any Drone, created by any `User`
3. As an `Administrator`, I can view all **False error** requests and accept or deny it

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
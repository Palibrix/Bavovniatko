----
anon: `Anonymous`
user: `User`
admin: `Administrator`
manager: `Manager`

as_an: As an `Anonymous`, I can
as_u: As a `User`, I can
as_u_will: As a `User`, I will
as_m: As a `Manager`, I can
as_ad: As an `Administrator`, I can

request: **Suggestion request**
list: **Part list**

p_or_d: Part or Drone
----

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
3. [ ] Filter: filter any {{p_or_d}} by item-specific values
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


include::docs/v1.md


include::docs/v2.md


include::docs/v3.md


include::docs/v4.md

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
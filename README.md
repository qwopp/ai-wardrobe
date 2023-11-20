# AI wardrobe - Virtuwear

# Virtuwear demonstration video: https://youtu.be/tSgxeQMFvnA

Virtuwear is a web-application where users can store and manage their clothing online. This web-app implements machine learning models in order to analyze images uploaded by the user, and categorize them automatically. Clothes are then stored on the database where they can easily be accessed. The other main feature of this web-app is outfit recommendations based on prompts. When the user enters a prompt in the box, we prompt the UM-GPT to find an outfit based on this prompt using the clothes in the user's wardrobe. The outfit it recommends will be displayed below, usually in head-to-toe order.

Built using React for the front-end, Flask for the back-end, and SQLite for the database. 
## Quick start

```console
$ ./bin/wardrobeinstall
$ ./bin/wardrobedb create
$ ./bin/wardroberun
```

# A-Lonely-Soul
A discord currency and RPG bot

[INVITE LINK](https://discordapp.com/api/oauth2/authorize?client_id=687476783297462312&permissions=8&scope=bot)

TODO:
- add better moderation commands (mute)
- add recipes for creating items 
- fix inventory instance var in User class because Python 
cannot deal with multi-layered objects. 
    - change it so that inventory items are compressed to integers
    - will make save files easier as well
    - bit operations on items.
    - OTHER METHOD: superclass USERLIST that contains 1 var = list of users

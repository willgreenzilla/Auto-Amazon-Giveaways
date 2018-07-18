# Auto-Amazon-Giveaways

This was forked from sniffingpickles whom forked from zdrouse and then modified a little by myself.

## Install
[Python 3.6.x](https://www.python.org/downloads/) must be installed.

After Python is installed, open `command-prompt` and use `pip` to install dependencies from project folder:

 - `pip install -r requirements.txt`

Assuming `git` is installed on the local machine:

 - Open `command-prompt` and `cd` to a location/folder to save the project.
 - Perform `git clone https://github.com/zdrouse/Auto-Amazon-Giveaways`.

## To Run
Rename the EDIT_ME_creds.json file (in the lib dir) to creds.json and edit the creds.json file:

- Change amazonemail@address.com to your Amazon account email address.
- Change amazonpassword to your Amazon account password.
- Change page_counter value to the page you wish to begin on if not the first page... This will increment as it runs and give the script a place to begin when it crashes and auto re-launches (via the loop.py).

Navigate into the Auto-Amazon-Giveaways directory via command prompt and type:

- python loop.py "give_it_away_now.py"

## Profit
![bezos](http://i.imgur.com/L8yRHGN.jpg)

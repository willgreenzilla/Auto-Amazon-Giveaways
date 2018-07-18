# Auto-Amazon-Giveaways

Implementation for this project is currently a work-in-progress.  Issues are expected.

This was forked from sniffingpickles whom forked from zdrouse.

## Install
[Python 3.6.x](https://www.python.org/downloads/) must be installed.

After Python is installed, open `command-prompt` and use `pip` to install dependencies from project folder:

 - `pip install -r requirements.txt`

Assuming `git` is installed on the local machine:

 - Open `command-prompt` and `cd` to a location/folder to save the project.
 - Perform `git clone https://github.com/zdrouse/Auto-Amazon-Giveaways`.

## To Run
Rename the EDIT_ME_creds.json file (in the lib dir) to creds.json and edit the creds.json file:

> Change amazonemail@address.com to your Amazon account email address.
> Change amazonpassword to your Amazon account password.
> Change numberofpages to the NUMBER of total giveaway pages. This is located at the bottom of https://www.amazon.com/ga/giveaways and will be displayed as something like [1][2][3] ... [135][Next]. 135 would be the total page count so enter this number.

Navigate into the Auto-Amazon-Giveaways directory via command prompt and type:

python loop.py "give_it_away_now.py"

## Profit
![bezos](http://i.imgur.com/L8yRHGN.jpg)

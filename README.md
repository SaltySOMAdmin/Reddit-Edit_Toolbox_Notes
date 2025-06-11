# Reddit-Edit_Toolbox_Notes
 
### This is a script designed to download, decrypt, and decompress Toolbox Modnotes
- DownloadUsernotes.py downloads and decompresses the Toolbox Modnotes into a json text file.
- UploadUsernotes.py takes a backup then recompresses and uploads the edited ModNotes to the Toolbox wiki page.

# Setup

## Setup a Linux Host
I'm using Ubuntu LTS on an Oracle Cloud VM. There are free-tiers available as of today. Google Compute and Amazon AWS are similar products. You can also roll your own host with an old PC or a Raspberry Pi. You'll need to know a bit of Linux CLI or you'll need to be ready to learn! Run these commands through the CLI.

## Setup Git
1. [Create a Github account.](https://github.com/join)

2. [Go here and install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) if you don’t have it already.

3. [Assuming you're reading this on the repo page](https://github.com/SaltySOMAdmin/Reddit-Edit_Toolbox_Notes), select ‘fork’ to create a copy of it to your Github account. 

4. From your new repo, select **Code** and then under **Clone** copy the HTTPS URL (e.g. https://github.com/SaltySOMAdmin/Reddit-Edit_Toolbox_Notes.git) to download a local copy

5. Navigate to a folder you want a local copy of the repo to live, and clone the Github repo to your host:
   1. It's up to you where to put the repo - recommended in a folder like /home/YourUserAcct/Github/ or /home/YourUserAcct/. Once you clone the directory it will create a subfolder with the name of your fork.
   2. git clone `<url>`
      1. e.g. git clone https://github.com/SaltySOMAdmin/Reddit-Edit_Toolbox_Notes.git

## Install necessary software prerequisites: 

1.  Install Python3

		sudo apt install python3

2.  Create a python virtual environment in a directory

		/usr/bin/python3 -m venv /home/ubuntu/Reddit-Edit_Toolbox_Notes

3.  Use the virtual python3 environment

		source /home/ubuntu/Reddit-Edit_Toolbox_Notes/bin/activate

4.  Install PIP Prereqs

		pip3 install praw
	


## Configure the script.
- There are several sections you need to customize in the two scripts. (DownloadUsernotes.py & UploadUsernotes.py) Edit them with a text editor and save.

- Logging paths, subreddit_name, and config.py will need to be updated with your credentials. 

# Running the scripts.
1.	Run the script via "source /home/ubuntu/Reddit-Edit_Toolbox_Notes/bin/activate" then "python DownloadUsernotes.py"
2.	This will download the current user notes into "usernotes.txt" then it will decompress the file into something we can read - "decompressed_usernotes.txt"
3.	Copy the text from "decompressed_usernotes.txt" into a JSON editor like: https://jsoneditoronline.org/
4.	Edit the JSON. Copy the edited json to a new file with whatever name makes sense to you. (edited_usernotes.txt)
5. 	Run the upload script "python UploadUsernotes.py" and specify your file name from step 4. 
6.  This will create another backup of the current usernotes (usernotes_backup-date.txt), recompress the JSON, and upload it to the wiki page. 

## Setup Continuous Deployment with Github Actions

Allows you to deploy your code via Github vs logging into the VPS and updating the code/uploading a new file. Allows for easier collaboration as well. I followed a guide similar to this one:
https://docs.github.com/en/actions/use-cases-and-examples/deploying/deploying-with-github-actions

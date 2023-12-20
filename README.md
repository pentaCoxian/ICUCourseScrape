
Install mariadb using script. Follow prompts for initial setup.

```
sudo apt install mariadb-server
sudo mysql_secure_installation
```

Make access User. Adjust `username` and `passwordForUser` acordingly.

```
sudo mariadb

CREATE USER username@'%' IDENTIFIED BY 'passwordForUser';
CREATE DATABASE databaseName;
GRANT ALL ON databaseName.* TO username@'%';
FLUSH PRIVILEGES;
QUIT;
```

Install mariadb connector-c. [Install CS package](https://mariadb.com/docs/connect/programming-languages/c/install/)

> [!NOTE]
> If the above doesn't work, try `sudo apt-get install libmariadb3 libmariadb-dev`

Install google chrome. chromedriver only exists to ver 114 so lock version to that.

```
wget https://www.slimjet.com/chrome/download-chrome.php?file=files%2F104.0.5112.102%2Fgoogle-chrome-stable_current_amd64.deb
# rename file
mv download-chrome.php\?file\=files%2F104.0.5112.102%2Fgoogle-chrome-stable_current_amd64.deb google-chrome-stable_104_amd64.deb
sudo dpkg -i  google-chrome-stable_104_amd64.deb
```
find matching major version chromedriver from [Here](https://chromedriver.chromium.org/downloads).

activate python venv

```
cd ./icuCourseScrape
python3.11 -m venv venv

source venv/bin/activate
```

install packages.

```
pip install mariadb selenium webdriver_manager beautifulsoup4 pandas sqlalchemy lxml
```

Finally, run script with:

```
python insert_data.py
```

all courses should be in the courses table in mariadb.

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

install python3.11 (ubuntu20.04)

```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-dev python3.11-venv
```

check python and pip versions

```
python3.11 -V
python3.11 -m pip -V
```

activate python venv.

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

## Others

- helper.pyの段階でデータは取得できていてinsert_data.pyでmariadbに入るよう調節しているだけなのでhelper.pyから直接別のドキュメントベースのDBなりに宛先変更したりしてもいいと思う。
- Dockerは対応できるだろうけどやるのめんどくさいので気分が向くまで放置されます。プルリク歓迎。

## Syllabi and mroonga

This will create a user that can access databaseName from anywhere, but mariadb will still refuse connections from outside local host. Therefore, go to mariadb config file. In my case it was `/etc/mysql/mariadb.conf.d/50-server.cnf`. Open it with sudo nano(or Vim if you want to look cool or something). Under `[mysqld]` find `bind-address=127.0.0.1`. comment it out. 

Next, this isn't nessesary for mariadb installation, as we're in the config file, we can add config for mroonga. Under `[mysqld]`, add this to the end.

```
innodb_ft_min_token_size=1
ft_min_word_len=1

innodb_buffer_pool_size=1024M
innodb_log_file_size=1G

server-id=100
max_connect_errors=10000
max-connections=500
```

## Installing mroonga

Again, before installing mroonga engine, make shure that the os is a version supported by mroonga. Supported OS versions can be seen [here](https://mroonga.org/docs/install.html). The setup in hte next section is for Ubuntu 20.04.

Mroonga should be bundled with maradb but I've never seen it. So, to install, first enable universe and security repo in ubuntu.

```
sudo apt-get install -y -V software-properties-common lsb-release
sudo add-apt-repository -y universe
sudo add-apt-repository "deb http://security.ubuntu.com/ubuntu $(lsb_release --short --codename)-security main restricted"
```

Then, add PPA to repo

```
sudo add-apt-repository -y ppa:groonga/ppa
sudo apt-get update
```

Finally install mroonga for mariadb aswell as MeCab for Japanese Tokenize

```
sudo apt-get install -y -V mariadb-server-mroonga
sudo apt-get install -y -V groonga-tokenizer-mecab
```

That's all! congrats you now should have mroonga installed on mariadb.

```
sudo mariadb
MariaDB [(none)]> SHOW ENGINES;
+--------+---------+----------------------------------------+
| Engine | Support | Comment                                | 
+--------+---------+----------------------------------------+
| Mroonga| YES     | CJK-ready fulltext search, column store|
| InnoDB | DEFAULT | Supports transactions, row-level loc...|
+--------+---------+----------------------------------------+
9 rows in set (0.000 sec)
```

To enable access from local servers, 

> [!TIP]
> If the program connecting to mariadb is on a different server, under [mysqld] find bind-address=127.0.0.1 and comment it out as well as opening ufw to the specific ip address.

For the changes to take place.

```
sudo systemctl restart mariadb
sudo systemctl restrt ufw
```



## MeCab config

mecabrc will be missing. this folder likely will be in `/etc/mecabrc` for some reason. Thus, copy the folder to what mecab wants `sudo cp /etc/mecabrc /usr/local/etc`.


noteable: https://engineering.linecorp.com/ja/blog/mecab-ipadic-neologd-new-words-and-expressions/
https://qiita.com/katsuyuki/items/65f79d44f5e9a0397d31
https://32imuf.com/sqlalchemy/note/  -> add full text index to TEXT is possible?

install dict using `sudo apt install mecab libmecab-dev mecab-ipadic-utf8 git make curl xz-utils file`
for better dictionaries, install ipadic-neologd 

```
sudo apt install mecab libmecab-dev mecab-ipadic-utf8 git make curl xz-utils file
git clone https://github.com/neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd
sudo bin/install-mecab-ipadic-neologd
```

to find dict location, `sudo find / | grep mecab-ipadic-neologd`
## SQLAlchemy

Setup example
```
engine = sa.create_engine("mariadb+mariadbconnector://python:pythonAccess56@172.31.54.136:3306/syllabusdb?charset=utf8mb4",echo=True)
Base = declarative_base()

class Course(Base):
    __tablename__ ="testtable"
    __table_args__ = {
        'mariadb_ENGINE': 'mroonga',
        'mariadb_DEFAULT_CHARSET': 'utf8mb4'
    }
    regno = sa.Column(sa.Integer, primary_key=True)
    title_j = sa.Column(sa.String(length=15900))
    title_e = sa.Column(sa.String(length=400))
```


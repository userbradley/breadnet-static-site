---
title: How to install kanboard
slug: how-to-install-kanboard
date: 2020-06-10T13:21:43.000Z
date_updated: 2021-05-02T01:47:43.000Z
summary: How to install kanboard on Ubuntu with Nginx
---

I have been using Kanboard for around 4 months to manage my internal tasks as well as organise my self. Think of it like a ticket at a restaurant that gets moved to different cooks so they know what needs to be done.

I will be using Ubuntu 18.04 for this, but it's the same for most version of Ubuntu.

Start with installing all the services we need. If you already have these installed on your server, you can skip this step

> It is worth noting that you can cause issues if you install different version of PHP on your server if it's already installed

    sudo apt-get update
    sudo apt-get upgrade -y
    sudo apt-get install nginx mariadb-server mariadb-client
    sudo apt install -y php7.2 php7.2-mysql php7.2-gd php7.2-mbstring php7.2-common php7.2-opcache php7.2-cli php7.2-xml

We also need to install certbot so we can get free SSL

    sudo apt-get install software-properties-common
    sudo add-apt-repository universe
    sudo add-apt-repository ppa:certbot/certbot
    sudo apt-get update
    sudo apt-get install certbot python3-certbot-nginx

Now that's done, we need to enable the services to start on boot

    sudo systemctl enable nginx
    sudo systemctl enable mariadb-server

Download and install Kanboard from Github

    sudo -s
    cd /var/www/
    sudo git clone https://github.com/kanboard/kanboard.git
    sudo chown -R www-data:www-data kanboard/data

Now this is where it becomes a little bit interesting as you need to do stuff on SQL.

    sudo mysql_secure_installation

Answer the following for the questions

    Enter current password for root (enter for none): Enter
    Set root password? [Y/n]: Y
    New password: <secure password>
    Re-enter new password: <secure password>
    Remove anonymous users? [Y/n]: Y
    Disallow root login remotely? [Y/n]: Y
    Remove test database and access to it? [Y/n]: Y
    Reload privilege tables now? [Y/n]: Y

Now we can create the database, user and import the schema

    mysql -u root -p -e "CREATE DATABASE kanboard;"
    mysql -u root -p kanboard < /var/www/kanboard/app/Schema/Sql/mysql.sql
    mysql -u root -p -e "CREATE USER 'kanboarduser'@'localhost' IDENTIFIED BY 'superdupersecretpassword';"

    mysql -u root -p -e "GRANT ALL PRIVILEGES ON kanboard.* TO 'kanboarduser'@'localhost' IDENTIFIED BY 'superdupersecretpassword' WITH GRANT OPTION;"

    mysql -u root -p -e "FLUSH PRIVILEGES;"

If you know how, you can login and run these commands your self opposed to doing it from the command line.

Next, edit `/etc/nginx-sites-available/kan.example.com` where `example.com` is your domain.  Same goes for the below which should be pasted in to the file `kan.example.com` , you will need to change the domain.

    server {
            listen       80;
            server_name  kan.example.com;
            index        index.php;
            root         /var/www/kanboard;
            client_max_body_size 32M;

            location / {
                try_files $uri $uri/ /index.php$is_args$args;
            }

            location ~ \.php$ {
                try_files $uri =404;
                fastcgi_split_path_info ^(.+\.php)(/.+)$;
                fastcgi_pass unix:/var/run/php/php7.2-fpm.sock;
                fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
                fastcgi_index index.php;
                include fastcgi_params;
            }

            location ~* ^.+\.(log|sqlite)$ {
                return 404;
            }

            location ~ /\.ht {
                return 404;
            }

            location ~* ^.+\.(ico|jpg|gif|png|css|js|svg|eot|ttf|woff|woff2|otf)$ {
                log_not_found off;
                expires 7d;
                etag on;
            }

            gzip on;
            gzip_comp_level 3;
            gzip_disable "msie6";
            gzip_vary on;
            gzip_types
                text/javascript
                application/javascript
                application/json
                text/xml
                application/xml
                application/rss+xml
                text/css
                text/plain;
        }

Once this has been done, we need to symlink it to the sites-enabled folder.

    sudo ln -s /etc/nginx/sites-available/kan.exmaple.com /etc/nginx/sites-enabled/kan.exmaple.com

Almost done!

You will need to edit the `config.php` file under `/var/www/kanboard` to tell Kanboard where the database is as we're using Mysql.

    sudo cp /var/www/kanboard/config.default.php /var/www/kanboard/config.php

Edit it

    nano /var/www/kanboard/config.php

In there you should find the below and edit it to reflect what we configured in the database from before.

> You will need to change `DB_DRIVER` and `DB_PASSWORD`

    // Database driver: sqlite, mysql or postgres (sqlite by default)
    define('DB_DRIVER', 'mysql');

    // Mysql/Postgres username
    define('DB_USERNAME', 'kanboard');

    // Mysql/Postgres password
    define('DB_PASSWORD', 'StrongPassword');

    // Mysql/Postgres hostname
    define('DB_HOSTNAME', 'localhost');

    // Mysql/Postgres database name
    define('DB_NAME', 'kanboard');

Now we can restart nginx.

    sudo systemctl restart nginx

Make sure you have got a DNS record pointing to your server. You will want an A record with the value being `kan` and the value being the IP address of your server

Once that is done, wait a few minutes depending on your DNS provider it may take up to 48 hours but in 2020, that shouldn't happen!

Go to <http://kan.example.com> and login with

Username: `admin`
Password: `admin`

To reset the password, go to `Admin` > `Users Management` > `Admin` > `Change password`
![](__GHOST_URL__/content/images/2020/06/image-12.png)![](__GHOST_URL__/content/images/2020/06/image-13.png)
Now, it's all good and well having this on the internet, but we want to be able to have some security. For this we will be using Lets Encrypt.

    certbot --nginx -d kan.example.com

Press 2 when asked. You shouldn't need to edit anything or restart anything but you're welcome to if wanted.

If you have any issues or something looks wrong, please contact me!

---

You can hire me via [Upwork](https://www.upwork.com/freelancers/~01c61ee9802b94133e) or [emailing me](mailto:work@breadnet.co.uk) for weekend projects!

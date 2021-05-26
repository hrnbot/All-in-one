# Deployment of Landing page/Blog

In digital marketing, a landing page is a standalone web page, created specifically for a marketing or advertising
campaign. It’s where a visitor “lands” after they click on a link in an email, or ads from Google, Bing, YouTube,
Facebook, Instagram, Twitter, or similar places on the web.

Unlike web pages, which typically have many goals and encourage exploration, landing pages are designed with a single
focus or goal, known as a call to action (or CTA, for short).

It’s this focus that makes landing pages the best option for increasing the conversion rates of your marketing campaigns
and lowering your cost of acquiring a lead or sale.

# Deployment

## Install Apache

Install the apache2 package:

```shell
$ sudo apt update
$ sudo apt install apache2
```

## Configure Firewall

|  WARNING: **Run** ```$ sudo ufw status``` do not enable if ```Status: active``` |
| --- |

```shell
$ sudo ufw enable
$ sudo ufw allow 22 #Make sure to open this port if using ssh else you won't be able to ssh in it.
$ sudo ufw allow 'Apache'
```

 ```jupyter
Output: 
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
22                         ALLOW       Anywhere
5000                       ALLOW       Anywhere
80                         ALLOW       Anywhere
Apache                     ALLOW       Anywhere
22/tcp (v6)                ALLOW       Anywhere (v6)
22 (v6)                    ALLOW       Anywhere (v6)
5000 (v6)                  ALLOW       Anywhere (v6)
80 (v6)                    ALLOW       Anywhere (v6)
Apache (v6)                ALLOW       Anywhere (v6)
``` 

## Check Apache is working

```shell
$ sudo systemctl status apache2
```

|  WARNING:  If not ``` active (running)``` then **Run** ```sudo systemctl start apache2```  |
| --- |

## Testing apache

[http://your_server_ip](http://localhost)

### Output

![alt text](https://github.com/hrnbot/Start-up/blob/main/images/small_apache_default.png?raw=true)

## Set Host

### clone your Repository

```shell
$ sudo cd /var/www
$ sudo git clone repo_link
$ ls 
```

```shell
Output:
blog
```

```shell
$ cd blog
$ ls
```

```shell
Output:
README.md  assets  css  favicon.ico  index.html  js
```

|  Note: We will consider repo name is ``` blog ``` and it contains one ``` index.html``` file |
| --- |

### Assign ownership of the directory

```shell
$ sudo chown -R $USER:$USER /var/www/your_domain
$ sudo chmod -R 755 /var/www/your_domain  #give permission
```

### Edit configuration file

```shell
$ sudo nano /etc/apache2/sites-available/blog.conf
```

|```/etc/apache2/sites-available/blog.conf```|
|---|

```
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName blog
    ServerAlias blog
    DocumentRoot /var/www/blog
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

### Enable current Blog

```shell
$ sudo a2ensite your_domain.conf
$ sudo a2dissite 000-default.conf #Disables Default Page
$ sudo apache2ctl configtest #To test Configuration
```

```shell
Output:
Syntax OK
```

```shell
$ sudo systemctl restart apache2
```

## Testing apache

[http://your_server_ip](http://localhost)

# Disable Blog

```shell
$ sudo a2dissite blog.conf
```
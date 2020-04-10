Original readme file was written in markdown, for better visualization, please refer to our team's Github page. 
https://github.com/KaiminOng/EsdWatchDog

# Watchdog README
# Requirements
	- docker-compose 3.7+
	- WAMP / Nginx (optional for creating virtual hosts)
	
# Setup
## Create your own Telegram Bot
1. Search for **@BotFather** on Telegram
2. In the chat with **@BotFather**, type `/start` to start the bot 
3. Type `/newbot` to create a new bot and enter the desired username for your Bot 

> *NOTE: Your bot name MUST end with the word "bot", e.g. TetrisBot or Tetris_bot*

4. You have successfully created your bot, and will be given a bot token
5. Set a domain name to link your bot to, E.g. http://esdwatchdog.me

> *NOTE: You should provide a fully qualified domain name (FQDN). If not, refer to the following instructions to create your own Virtual Host with WAMP*

## Create Your Own Virtual Host with WAMP
For this example, we will be using the **WAMP** stack for creating virtual hosts. However, you can use Nginx or  your preferred Apache stack.

1. Turn on WAMP
2. Type `localhost` into your internet browser of your choice and enter. 
3. Scroll down to **Tools** Section and select **Add a Virtual Host**
4. Follow the instructions given on the page and complete the creation of your Virtual Host
5. Ensure the following ports are unused on your machine
	- **80 (Webapp)**
	- **1337 (Konga)**
	- **3306 (MySQL)**
	- **5002 (Healthcheck)**
	- **8000 (Konga)**
	- 8080 (Phpmyadmin)
	- 15672 (RabbitMQ Management UI)
	
>*Services not bolded are optional and are not essential for the Watchdog app. However, if you choose to omit them remember to comment out these services in the `docker-compose.yml` file.*

## Change environment variables

In `/env/.env.prod`, change the following variables:

`WEBHOOK_ROUTE=/<BOT-TOKEN>`  
>Use the bot token of your own telegram bot.
## Webapp Configuration
In `/webapp/config.php`, change the following variables

```
# Telegram bot
$bot_username  -  Telegram Bot username
$bot_token     -  Telegram Bot token

# Domain configuration
$domain_name   -  Domain name
$hostname      -  Endpoint URI for kong service
```
# Build
Open terminal of your choice, for this example we will be using **Bash**. Navigate to the project root and run

`docker-compose up -d --build`

The build process will take anywhere from 5 to 10 minutes depending on your internet connection and hardware. Once the build process has finished, run 

`docker ps` 

To check the state of your containers. If there some containers which are unhealthy, they could be raising errors since prerequisite services (RabbitMQ, SQL)may not be running yet. 

However, if the container still refuses to boot, you can run

```
docker-compose logs -f               --- View collective logs
docker logs -f <container_id>        --- Logs for single container
```

# Kong Configuration
After setting setting up the containers, we need to configure the Kong API gateway will require some additional configuration. 

## Creating an upstream service
1. Click on the **Services** tab on the sidebar
2. Add a new service with endpoint http://watchlist:5001
3. Configure the following routes for the service


| Route | Method | Protocol | 
|:--------:| :-------------:| :-------------:|
| /watchlist/remove | POST |  HTTP
| /watchlist/new | POST, OPTIONS | HTTP
| /contact/get | GET | HTTP
| /watchlist/get | GET | HTTP


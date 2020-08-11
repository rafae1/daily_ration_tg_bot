# Daily ration in telegram bot
A small project for my wife. She is interested in a healthy lifestyle and asked me to copy recipes from a (secret) site and create a bot in telegram that could give out a daily diet or any random food from the database. I hid access to the site, username and password, and left only the code which I used for scrapping. Also I left the database. If you specify your telegram_id and bot token, you can use it. All recipes are presented in Russian.

<strong>Using:</strong><br />
./docker_install.sh<br />
docker-compose up -d --build

<strong>Roadmap:</strong><br />
1. Fix work with file system (use threadpools)
2. Use postgres instead of SQLite
3. Use async ORM, e.g. PonyORM
4. Add route to add own recipe

#!/usr/bin/env bash
#Install Nginx if not already in
if ! command -v nginx &> /dev/null
then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

echo "<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>This is a test page for Nginx configuration</h1>
</body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

nginx_config="server {
    listen 80;
    server_name _;
    location /hbnb_static {
        alias /data/web_static/current/;
        index index.html index.htm;
    }
}"

sudo bash -c "echo \"$nginx_config\" > /etc/nginx/sites-available/default"

sudo service nginx restart

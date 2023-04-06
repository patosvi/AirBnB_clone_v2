#!/usr/bin/env bash
#Bash Script that configures Nginx server with some folders and files

html="
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
"
# Update package information and install Nginx
sudo apt-get -y update
sudo apt-get -y install nginx

# Start the Nginx service
sudo service nginx start

# Create necessary directories for website deployment
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Add the HTML content to an index.html file in the deployment directory
printf "%s" "$html" >> /data/web_static/releases/test/index.html

# Create a symbolic link to the deployment directory in /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership of the /data/ directory to the user "ubuntu"
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n' /etc/nginx/sites-available/default

# Restart the Nginx service to apply the changes to the configuration
sudo service nginx restart


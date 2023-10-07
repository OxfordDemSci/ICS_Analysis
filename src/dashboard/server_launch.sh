# DGG launch script to configure server

# hostname
sudo hostnamectl set-hostname shapeimpact

# update
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get auto-remove -y && sudo reboot now

sudo crontab -e
# @weekly apt-get update -y && apt-get upgrade -y && apt-get auto-remove -y

#---- docker ----#

# install docker
sudo apt-get install ca-certificates curl gnupg lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
sudo apt-get update && \ 
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-compose

# add user to docker group
sudo usermod -aG docker ubuntu
newgrp docker


#---- github ----#
sudo apt install git

# create GitHub deploy key
cd ~/.ssh
ssh-keygen

#!! Remember to authorize the key on GitHub

# ssh config for github
echo "Host github" >> ~/.ssh/config
echo -e "\tHostName github.com" >> ~/.ssh/config
echo -e "\tUser git" >> ~/.ssh/config
echo -e "\tIdentityFile ~/.ssh/id_rsa" >> ~/.ssh/config

# clone repository
cd ~
git clone git@github.com:OxfordDemSci/ICS_Analysis

# deploy
cd ~/ICS_Analysis/src/dashboard
docker-compose up -d --build




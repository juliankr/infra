# install zsh

sudo apt install zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"



# install docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

 sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# mount raid https://www.techrepublic.com/article/how-to-properly-automount-a-drive-in-ubuntu-linux/

sudo apt-get install silversearcher-ag

sudo apt install jq
sudo apt install network-manager

# https://pimylifeup.com/raspberry-pi-dns-server/

# install certbot to create certificates
sudo snap install --classic certbot

# install strato-certbot
git clone git@github.com:Buxdehuda/strato-certbot.git

mkdir nginx_data/cache
mkdir nginx_data/run
mkdir nginx_data/tmp

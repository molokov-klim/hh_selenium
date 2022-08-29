ssh root@{IP}
{PASS}

apt install sudo /n
sudo apt update && sudo apt upgrade

sudo adduser {USER}
{PASS}

cd /etc/sudoers
visudo sudoers
#add {USER} user to sudoers
#or try sudo usermod -aG sudo {USER}

su {USER}

cd /home/{USER}
mkdir projects
cd projects
mkdir hh_selenium
cd hh_selenium

sudo apt install python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -U setuptools
pip install -U selenium
sudo apt install -y libxss1 libappindicator1 libindicator7
sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb
sudo apt install -y -f
sudo apt install screen
google-chrome --version

#upload files by FILEZILLA or scp

sudo chmod +x chromedriver

python3 hh_selenium.py

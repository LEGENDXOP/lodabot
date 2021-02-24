
echo "
	              Hmmm 🤔💘

	    °•° Deployment Begins •°•
"
echo '
        •• Getting Packages and Installing bot
'

export DEBIAN_FRONTEND=noninteractive
export TZ=Asia/Kolkata
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

apt-get update
apt-get upgrade -y
apt-get install -y --no-install-recommends ffmpeg neofetch mediainfo megatools
apt-get autoremove --purge

echo '
        •• Cloning Repository
'
git clone https://github.com/Amarnathcdj/lodabot.git /root/lodabot/

echo '
	•• Getting Libraries and Installing
'
pip install --upgrade pip setuptools wheel
pip install search-engine-parser==0.6.2
pip install -r /root/lodabot/requirements.txt

echo "

			      Loda Bot 69.69

			•°• Deployed Successfully °•°
		   •• Wait till python images are pushed
	   •• Give build logs in @dclogger if build fails
"

Делал backend, фронтом особо не заморачивался.

Логин/пароль к сайту http://188.120.225.94:
user: admin
pass: 012346789
Для просмотра нужна ширина дисплея не менее 1000рх (десктоп).
Мобильный вариант не прорабатывал.
Сделал два репозитория: один для продакшана, второй для лок разработки.
ssl не стал настраивать, для тестового он не нужен.
SECRET_KEY, логины, пароли выложил на git (знаю, что так не делают) для быстроты разворачивания.

Инструкция по разворачиванию в продакшн:
#создать пользователя
adduser admin
usermod -aG sudo admin
#установить cURL
sudo apt-get update
sudo apt-get install curl
# Установить docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
# Установить докер
sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
# Запустить демон Docker и активировать его автозапуск:
sudo systemctl start docker
sudo systemctl enable docker
#Установить git
sudo apt-get install git

#клонировать репозиторий
git clone https://github.com/Al-exanderr/employeess_prod.git
cd employeess_prod
# добавить ip сервера в .env.dev/allowed_hosts
# запустить docker-compose
sudo docker-compose -f docker-compose.yml up -d --build
#Если с первого раза не заработал, перезапустить.



Инструкция по разворачиванию в деплой:
аналогична приведённой для продакшана, только другой дистрибутив:
git clone https://github.com/Al-exanderr/employeess_dev.git

Буду очень благодарен за фидбек.


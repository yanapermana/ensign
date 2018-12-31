# ENSIGN (Education and Network Security w/ IGNiter)

Interactive Multimedia based on Capture The Flag Game with Problem Based Learning Model using Boyer-Moore Algorithm to Improve Comprehension of SMK Students in Network Security Materials 

## Install

```
sudo pip install --upgrade pip
sudo apt install python-cairo libcairo2-dev
sudo pip2 install -r requirements.txt
sudo python manage.py makemigrations
sudo python manage.py migrate

cd /tmp/
git clone https://github.com/vishnevskiy/bbcodepy
cd bbcodepy/
ls
sudo python setup.py install


sudo python manage.py runserver 0:8000
sudo ln -s /home/dummy/ensign/ensign.conf /etc/supervisor/conf.d/
sudo supervisorctl reread && sudo supervisorctl update && sudo supervisorctl status
```

## Depedencies

* [bbcodepy](https://github.com/vishnevskiy/bbcodepy)

## License

* See LICENSE file

## Todo

* Update License

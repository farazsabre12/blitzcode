# setup
make sure python is installed.
make a new folder, say blitz
create a virtual env

```sh
cd blitz
python -m venv blitzenv
cd .\blitzenv\
.\Scripts\activate
cd ..
```


clone repo using  
```sh
git clone https://git.sabre-gcp.com/scm/~sg0703503/blitzcode-api.git
```



install requirements using
make sure you are on the path that contains requirements.txt
```sh
pip install -r requirements.txt
```
use to run server
```sh
fastapi dev main.py
```
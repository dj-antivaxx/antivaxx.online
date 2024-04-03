# antivaxx.online

4chan-but-cute, pure flask+html/css, lean and minimal, no javascript bullshit. hosted and maintained by dj antivaxx at www.antivaxx.online

## local start

clone the repo, install the requirements (`pip install -r requirements.txt`; i recommend using a separate python env), run from the root directory (`python src/app.py`). by default runs on port 8080 (http://127.0.0.1:8080). the database is populated to `artifacts`, all the uploaded pictures are populated to `uploads` and renamed, but the original filenames are stored in the database. 

## docker start

first need docker [(source)](https://docs.docker.com/engine/install/ubuntu/): 

```
sudo apt-get update

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

then clone this project to ur machine and build the container:

```
docker build . -t antivaxx:1
```

do `docker images` to checko the image id and then:

```
docker run -dit -p 5000:5000 <urimageid>
```

the website will be running at port 5000

in case something goes wrong - `docker ps -a` shows stopped containers, and u can copy the logs to a local text file like `logs.txt` via `docker cp <urcontainerid>:/home/tmp/report logs.txt` (works even if the container is stopped).  

## misc

feel free to reach out if u have any questions or inquries! “%s.%s@%s.%s” % ("dj", "antivaxx", “gmail”, “com”) or @dj_antivaxx on ig

yowza!

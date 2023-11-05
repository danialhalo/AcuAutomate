# AcuAutomate
**AcuAutomate** is an unofficial Acunetix CLI tool that simplifies automated pentesting and bug hunting across extensive targets. It's a valuable aid during large-scale pentests, enabling the easy launch or stoppage of multiple Acunetix scans simultaneously. Additionally, its versatile functionality seamlessly integrates into enumeration wrappers or one-liners, offering efficient control through its pipeline capabilities.

![alt text](https://raw.githubusercontent.com/danialhalo/AcuAutomate/main/banner.png)

## Installation
```
git clone https://github.com/danialhalo/AcuAutomate.git
cd AcuAutomate
chmod +x AcuAutomate.py
pip3 install -r requirements.txt
```

## Configuration (config.json)
Before using AcuAutomate, you need to set up the configuration file _config.json_ inside the **AcuAutomate** folder:
```JSON
{
    "url": "https://localhost",
    "port": 3443,
    "api_key": "API_KEY"
}
```


```
## Usage
The help parameter (-h) can be used for accessing more detailed help for specific actions
```
    		                               __  _                 ___
    		  ____ ________  ______  ___  / /_(_)  __      _____/ (_)
    		 / __ `/ ___/ / / / __ \/ _ \/ __/ / |/_/_____/ ___/ / /
    		/ /_/ / /__/ /_/ / / / /  __/ /_/ />  </_____/ /__/ / /
    		\__,_/\___/\__,_/_/ /_/\___/\__/_/_/|_|      \___/_/_/
    		
    		                   -: By Danial Halo :-

    
usage: AcuAutomate.py [-h] {scan,stop} ...

Launch or stop a scan using Acunetix API

positional arguments:
  {scan,stop}  Action to perform
    scan       Launch a scan use scan -h
    stop       Stop a scan

options:
  -h, --help   show this help message and exit
```

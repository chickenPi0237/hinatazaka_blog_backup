Hinatazaka Blog Backup
===
## Introdution
This project will download and backup every member's blog. Because of using sleep() function to slow down process, it may take a little longer (about an hour) to fully backup all blogs when first time executing program. 


## Dependecy
python 3.6  
[beautifulsoup4 4.8.1](https://pypi.org/project/beautifulsoup4/, "pypi beautifulsoup4")

- Note:
This project using [Anaconda](https://www.anaconda.com/download, "Anaconda officiall website") for environment management purpose.

## How to use
modify variable ***memberFolderPath*** to where you want to save then execute program.

`python memberblog.py`

Also, there is a *auto.bat* could be set in Windows Task Scheduler to automatically execute program. Before using *auto.bat*, there is something to modify by yourself and had been noted in *auto.bat*.
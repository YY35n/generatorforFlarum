# generatorforFlarum

activate the venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1


scrapy crawl forum -o posts.json


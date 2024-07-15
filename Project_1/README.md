
# Wiki Website

Do you know what a non-static website is?

In the previous exercise, we created a completely static website replicating google.com.

But imagine if Wikipedia were a static website. It would require an HTML file for each page, and users would need edit access to the HTML on the server, which would be a huge security breach.

That's why we have dynamic websites.

This allows us to add backend code to a website. In this project, I used Django, which is a Python framework.

## How to Start the Web Server

First, you need to check if you have Python installed.

On Ubuntu :
```sh
python3 --version
```

If it returns:
```sh
Command 'python' not found
```

Try:
```sh
sudo apt install python3
```

To install the Django framework:
```sh
sudo apt install python3-django
```

To install Markdown2 (used to transform the .md content to HTML code):
```sh
sudo apt install python3-markdown2
```

Please note that when installing a framework/library like this, it will be installed locally on the computer. You could also do this with an externally managed environment.

Of course, you need to clone the repository, then navigate to Project_1/:
```sh
python3 manage.py runserver
```

This will start the Django web server and make the wiki available in your web browser locally at localhost:8000 or 127.0.0.1:8000.


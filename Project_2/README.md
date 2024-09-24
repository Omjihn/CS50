
# Online market website

Previous exercise was fun but creating files to manage the data is kind of boring.

That's why we have databases, and guess what Django can handle SQL.

## Django Model Creation

It's just a class who inherit model Django built-in class.

Models will be added in the [models.py](/Project_2/auctions/models.py) file.

In this class you can define everything you need for example, in order to create a user model I will add a username, e-mail and a password.
  
Pretty simple right ?
  
Huummm not that much, in fact SQL have precise types and options for most of them, see the doc [here](https://docs.djangoproject.com/en/5.1/ref/models/fields/#model-field-types).

In all those types there is the foreign key, this one is like a pointer to another existing model.

For example if I have a comment fuctionality on my website, I add the foreign key to it and each times a user add one, the user will be linked to it's comment.

## How To Fill My DB Now ?

Thanks to Django no need to learn SQL syntax.

Since our models are python classes, we just need to initialize them and just call `.save()` (This is a basic example please use built-in Django user, and do not save passwords like this) :

```py
newUser = User(username='bgdu28', password='noleak')
newUser.save()
```

## Access Data In My DB

Each DB research can return 0, 1 or more items, you can order them by creation date for example.

For example if I want to find every user with the username Kevin:

```py
Users = User.objects.filter(username='Kevin')
```

## Start The Web Server

More infos in this [README.md](Project_1/#how-to-start-the-web-server)

```sh
> python3 manage.py runserver
```

## See and Modify DB With Django Admin Panel

First you need to define what should be displayed in the admin panel in the [admin.py](Project_2/auctions/admin.py) file.

Then you can create an Django admin user with this command :

```sh
> python3 manage.py createsuperuser
```

After this you can start the server, and access `localhost:8000/admin` in your web browser.

Just login and you should see all your models and be able to create, modify, and delete them.

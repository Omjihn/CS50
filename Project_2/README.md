
# Online market website

The previous exercise was fun but creating files to manage the data is kind of boring.
That's why we have databases, and guess what ? Django can handle SQL for us.

## Django Model Creation

In Django, a model is just a class that inherits from Django's built-in `Model` class. Models will be defined in the [models.py](/Project_2/auctions/models.py) file.

In this class, you can define all the fields you need. For example, to create a user model, you would define fields like `username`, `email`, and `password`.
  
Pretty simple, right ?
  
Huummm, not entirely, SQL has specific types and options for most fields. You can learn more about them in the doc [here](https://docs.djangoproject.com/en/5.1/ref/models/fields/#model-field-types).

One important field type is the **foreign key**, which acts as a pointer to another model. For instance, if your website has a comment feature, you can add a foreign key to the comment model. Each time a user adds a comment, the user will be linked to that comment via the foreign key.

## How To Fill My DB Now ?

Thanks to Django no need to learn SQL syntax. Since our models are just Python classes, you simply need to instantiate them and call the `.save()` method.

Here's a basic example, using Django built-in user model :

```py
newUser = User.objects.create_user(username, email, password)
newUser.save()
```

## Access Data In My DB

Database queries can return 0, 1, or more items. You can also sort them, for example, by creation date.

For instance, to find all users with the username "Kevin", you can use the following query:

```py
Users = User.objects.filter(username='Kevin')
```

## Start The Web Server

For more information, check out this [README.md](Project_1/#how-to-start-the-web-server)

```sh
> python3 manage.py runserver
```

## See and Modify DB With Django Admin Panel

First, you need to specify what should be displayed in the admin panel. This is done in the [admin.py](Project_2/auctions/admin.py) file.

Next, you can create a Django admin user with the following command:

```sh
> python3 manage.py createsuperuser
```

After this, start the server and go to `localhost:8000/admin` in your web browser. Log in with your admin credentials, and you will be able to view, create, modify, and delete all your models.

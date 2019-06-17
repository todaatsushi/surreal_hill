# Surreal Hill
Horror Writer Zeno Watts' Website - Made with Django & Wagtail CMS.

## Project links
* [Website](https://zenowatts.pythonanywhere.com) - link to the site
* [Project page](https://www.atsushi.dev/work/surreal-hill/) on atsushi.dev - link to more information on the project page on my site

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Installing

Using a virtual env (recommended), install dependancies from requirements.txt.

```
pip install -r requirements.txt
```
Then, just migrate the databases and you're good to go.
```
python manage.py migrate
```

## **Recommended**:
```
python manage.py createsuperuser
```

to use admin functionalities e.g. create pages.

## .env variables
Surreal Hill expects the following variables:

* SECRET_KEY - Django secret key
* DEBUG - 'True' for debug mode


## Extra installation notes
* The whole structure of the site is built around Wagtail's [Page Model system](https://docs.wagtail.io/en/v2.5.1/topics/pages.html). This means without a user defined structure, the site has no skeleton to base on.

This site has:
### Top level pages
* Home page
* Work page (Types of content)
* Form page (With a contact form field)

### Secondary pages
#### Blog / articles & stories
* Blog index page
* Story index page

#### Image / meta data pages
* Tag index page
* Category index page
* Story main gallery image page
* Chapter gallery image page
* Article gallery image page

### Content level pages
* Blog / article page
* Story main page

### Content sub level page
* (Story) Chapter page


## Deployment

To serve static files make sure [Whitenoise](http://whitenoise.evans.io/en/stable/django.html) is configured properly and run
```
python manage.py collectstatic
```

This site is hosted on PythonAnywhere which configures static files for you. To install Whitenoise and configure, run:
```
pip install whitenoise
```
And follow instructions from the [docs](http://whitenoise.evans.io/en/stable/django.html).

## Built With

* [Django](https://docs.djangoproject.com/en/2.2/) - The web framework used
* [Wagtail](https://docs.wagtail.io/en/v2.5.1/index.html) - Django based CMS framework
* [Bulma](https://bulma.io/) - CSS framwork

## Authors

* **Me, Atsushi Toda** - [GitHub](https://github.com/broadsinatlanta) - [Actual atsushi.dev site](https://www.atsushi.dev)

## License

This project is licensed under the MIT License.

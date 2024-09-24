# Migrations commands used in Terminal
## python manage.py makemigrations: Creates new migration files based on changes to models.
## python manage.py migrate: Applies migrations to the database.
## python manage.py migrate --fake: Marks a migration as applied without actually running it.
## python manage.py migrate --fake-initial: Marks the initial migration as applied without actually running it.
## python manage.py squashmigrations: Squashes multiple migrations into a single migration file.
## python manage.py showmigrations: Displays a list of all migrations and their status.
## python manage.py sqlmigrate: Displays the SQL code for a specific migration.
## python manage.py dbshell: Opens a database shell for the current database.
## python manage.py flush: Flushes the database, removing all data and resetting the schema.
## python manage.py dumpdata: Dumps data from the database into a JSON file.
## python manage.py loaddata: Loads data from a JSON file into the database.


<!--            these migrations can be applied for specific file in a specific app
                eg :- python manage.py migrate --fake shop 0001           -->




# templates/shop/index.html
## The aria-label attribute is used to provide an accessible label for screen readers, helping users who rely on these tools to understand what each button or element represents.
## Why Use aria-label="Slide {{i|add:1}}"?
## In the context of a Bootstrap carousel, the aria-label attribute on the slide buttons usually indicates which slide number the button will take the user to. Since the carousel uses zero-based indexing for data-bs-slide-to, you might want the aria-label to start counting from 1 for better accessibility.
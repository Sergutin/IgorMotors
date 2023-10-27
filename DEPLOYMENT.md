# **Deployment**

## Table of Contents

* [Create Repository](#create-repository)
* [Setting up the Workspace](#setting-up-the-workspace)
* [Creating ElephantSQL database](#creating-elephantsql-database)
* [Creating Heroku App](#creating-heroku-app)
* [AWS S3 Bucket](#aws-s3-bucket)
* [Creating Environmental Variables](#creating-environmental-variables)
* [Setting up settings.py file](#setting-up-settingspy-file)
* [Cloning and forking](#cloning-and-forking)


<p>I took the following steps to deploy the site to Heroku, along with the necessary console commands for initialization.</p>

  > pip3 install -r requirements.txt

  ### Create Repository

Create a new repository in GitHub and clone it locally following [these instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)

<li> If you are cloning this project, then you can skip all pip3 installs and just run the following command in the terminal to install all the required libraries/packages at once:</li>

If developing locally on your device, ensure you set up/activate the virtual environment ([see below](#setting-up-the-workspace)) before installing/generating the requirements.txt file; failure to do this will put other projects at risk.

  ### Setting up the Workspace
<li>Install Django with version 3.2:</li>

  > pip3 install django==3.2.20

<li>Install django-allauth for account authentication, registration, management, and third-party (social) account authentication:</li>

  > pip3 install django-allauth==0.41.0

<li>Install Django Crispy Forms:</li>

  > pip3 install django-crispy-forms==1.14.0

<li>Install Django Countries:</li>

  > pip3 install django-countries==7.2.1

<li>Install gunicorn:</li>

  > pip3 install gunicorn
<li>Install supporting libraries:</li>

  > pip3 install dj_database_url==0.5.0 psycopg2

<li>Create requirements.txt:</li>

  > pip3 freeze > requirements.txt

<li>Create a folder, and a project in that folder:</li>

  > django-admin startproject <your_project_name> (in my case, the project name was "igormotors")

<li>Create an app within the project:</li>

  > python3 manage.py startapp <your_app_name> (in my case, the app name was "igormotors")

<li>Add a new app to the list of installed apps in setting.py</li>

<li>Migrate changes:</li>

  > python3 manage.py migrate

<li>Test server:</li>

  > python manage.py runserver (You should see the default Django success page)

  ### Creating ElephantSQL database

<p>Assuming that the user has already created an account with ElephantSQL.</p>

<li>Click “Create New Instance”</li>

<li>Set up your plan. 
  <ul>Give your plan a Name.</ul>
  <ul>Select the plan.</ul>
  <ul>You can leave the Tags field blank.</ul>
</li>

<li>Select “Select Region”</li>

<li>Click “Review”</li>

<li>Check your details are correct and then click “Create instance”</li>

<li>Return to the ElephantSQL dashboard and click on the database instance name for this project</li>

  ### Creating Heroku App

<p>Assuming that the user has already created an account with Heroku.</p>

<li>Create a new Heroku app:</li>

  > Click "New" in the top right-hand corner of the main page, then click "Create new app"

<li>Give your app a name and select the region closest to you. When you’re done, click "Create app" to confirm</li>

<li>Open the "Settings" tab. Add the config var DATABASE_URL, and for the value, copy in your database url from ElephantSQL.</li>

<li>From your editor, go to your projects settings.py file and copy the SECRET_KEY variable. Add this to the same name variable under the Heroku App's config vars.</li>

  <ul>left box under config vars (variable KEY) = SECRET_KEY</ul>
  <ul>right box under config vars (variable VALUE) = Value copied from settings.py in project.</ul>

  ### AWS S3 Bucket  

<p>Assuming that the user has already created an account with AWS.</p>

<li>Create a new S3 bucket:</li>

  <ul>Click "Services" in the top left-hand corner of the main page, select "S3"</ul>

  <ul>Click "Create bucket", give the bucket a unique name</ul>

  <ul>Select the nearest location</ul>

  <ul>Under the "Object Ownership" section, select "ACLS enabled"</ul>

  <ul>Under the "Bucket settings for Block Public Access", uncheck "Block all public access", and acknowledge that this will make the bucket public</ul>

  <ul>Click "Create bucket"</ul>

<li>Bucket settings:</li>

  <ul>Click on the bucket name, and then on the "Properties" tab</ul>

  <ul>Under the "Static website hosting" section, click "Edit"</ul>

  <ul>Under the "Static website hosting" section select "Enable"</ul>

  <ul>Under the "Hosting type" section ensure "Host a static website" is selected</ul>

  <ul>Under the "Index document" section enter "index.html"</ul>

  <ul>Click "Save changes"</ul>

<li>Bucket permissions:</li>

  <ul>Click on the "Permissions" tab</ul>

  <ul>Scroll down to the "CORS configuration" section and click edit</ul>

  <ul>Enter the following snippet into the text box</ul>

    [
      {
          "AllowedHeaders": [
              "Authorization"
          ],
          "AllowedMethods": [
              "GET"
          ],
          "AllowedOrigins": [
              "*"
          ],
          "ExposeHeaders": []
      }
    ]

  <ul>Click "Save changes"</ul>

  <ul>Scroll back up to the "Bucket Policy" section and click "Policy generator"</ul>

  <ul>Select "S3 Bucket Policy" from the drop down menu</ul>

  <ul>Enter " * " in the "Principal" text box</ul>

  <ul>From the "Actions" drop down menu select "GetObject"</ul>

  <ul>Copy and paste the "ARN" from the bucket policy page into the "Amazon Resource Name (ARN)" text box.</ul>

  <ul>Click "Add Statement", and then "Generate Policy"</ul>

  <ul>Copy the policy and paste it into the bucket policy text box on the previous tab. In the same text box add "/*" to the end of the resource key to allow access to all resources in this bucket.</ul>

  <ul>Click "Save"</ul>

  <ul>Select "Access Control List" section, find "Public access" and click "Everyone" under it. In the "Access to the objects" pop up window, tick "List objects"</ul>

  <ul>Click "Save"</ul>

<li>Create AWS static files User and assign to S3 Bucket:</li>

  <ul>Create "User Group":</ul>

      Click "Services" in the top left-hand corner of the main page
    
      Under "Access management" click "Groups"

      Click "Create New Group", enter Group Name

      Scroll to the bottom of the page and click "Create Group"

  <ul>Create permissions policy for the new user group:</ul>

      Click "Policies" in the left-hand menu.

      Click "Create Policy"

      Click "Import managed policy"

      Search for "AmazonS3FullAccess", select this policy, and click "Import"

      Click "JSON" under "Policy Document" to see the imported policy

      Copy the bucket ARN from the bucket policy page and paste it into the "Resource" section of the JSON snippet. Be sure to remove the default value of the resource key ("*") and replace it with the bucket ARN.

      Copy the bucket ARN a second time into the "Resource" section of the JSON snippet. This time, add "/*" to the end of the ARN to allow access to all resources in this bucket

      Click "Review Policy"

      Enter a name for the policy and a description
      
      Click "Create Policy"

  <ul>Attach Policy to User Group:</ul>

      Click "Groups" in the left-hand menu

      Click on the user group name created during the above step
    
      Click "Attach Policy"

      Search for the policy created and select it

      Click "Attach Policy"

  <ul>Create User:</ul>

      Click "Users" in the left-hand menu

      Click "Add user"

      Enter a "User name" 

      Select "Programmatic access" and click "Next"

      Select "Add user to group"

      Click "Next"

      Click "Create user"

      Take note of the "Access key ID" and "Secret access key" as these will be needed to connect to the S3 bucket
    
      Click "Download .csv" to download the credentials

      Click "Close"

<li>Install required packages to use AWS S3 Bucket in Django:</li>

  > pip3 install boto3

  > pip3 install django-storages

<li>Add 'storages' to the bottom of the installed apps section of settings.py file:</li>

    INSTALLED_APPS = [
    …,
        'storages'
    …,
    ]

### Creating Environmental Variables 

<li>Create new env.py file on top level directory. Add this to the .gitignore file</li>

<li>In env.py - Import os library</li>

  > import os

<li>Set environment variables</li>

  > os.environ["DATABASE_URL"] = "Paste in ElephantSQL database URL"

<li>Add in secret key</li>

  > os.environ["SECRET_KEY"] = "Make up your own randomSecretKey"

<li>In heroku.com - Add Secret Key to Config Vars</li>

  > SECRET_KEY, “randomSecretKey”

### Setting up settings.py file

<li>At the top of your settings.py file, add the following:</li>

    import os
    from pathlib import Path
    import dj_database_url
    if os.path.isfile("env.py"):
      import env

<li>Add a conditional in setting.py DATABASES section by replacing it with the following snippet to link up the Heroku Postgres server when in production and SQLite3 when developing locally:</li>

    if 'DATABASE_URL' in os.environ:
        DATABASES = {
            'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }

<li>Tell Django to where to store media and static files by placing this under the comments:</li>

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/

    STATIC_URL = '/static/'
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

<li>Build paths inside the project:</li>

    BASE_DIR = Path(__file__).resolve().parent.parent

<li>Within TEMPLATES array, add 'DIRS':[TEMPLATES_DIR] like the below example:</li>

    TEMPLATES = [
          {
              …,
              'DIRS': [
                os.path.join(BASE_DIR, 'templates'),
                os.path.join(BASE_DIR, 'templates', 'allauth'),
        ],
              …,
              
            },
      ]

<li>Link S3 Bucket to Django Project by adding the following to the settings.py file:</li>

    if 'USE_AWS' in os.environ:
        # Cache control
        AWS_S3_OBJECT_PARAMETERS = {
            'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
            'CacheControl': 'max-age=94608000',
        }

        # Bucket Config
        AWS_STORAGE_BUCKET_NAME = 'igormotors'
        AWS_S3_REGION_NAME = 'eu-west-1'
        AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
        AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
        AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

        # Static and media files
        STATICFILES_STORAGE = 'custom_storages.StaticStorage'
        STATICFILES_LOCATION = 'static'
        DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
        MEDIAFILES_LOCATION = 'media'

        # Override static and media URLs in production
        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'

<li>Add allowed hosts to settings.py:</li>

      ALLOWED_HOSTS = ["PROJECT_NAME.herokuapp.com", "localhost", "127.0.0.1",
                      '.herokuapp.com',]

<li>Create Procfile at the top level of the file structure and insert the following:</li>

      web: gunicorn PROJECTNAME.wsgi:application

<li>Make an initial commit and push the code to the GitHub Repository</li>

      git add .
      git commit -m "Initial deployment"
      git push

<li>Add AWS Keys (see above) to Heroku Config Vars</li>

<li>Add the USE_AWS variable to Heroku Config Vars and set it to True</li>

<li>Create a file called "Custom_storages.py" in the root of the project and add the following code:</li>

      from django.conf import settings
      from storages.backends.s3boto3 import S3Boto3Storage


      class StaticStorage(S3Boto3Storage):
          location = settings.STATICFILES_LOCATION


      class MediaStorage(S3Boto3Storage):
          location = settings.MEDIAFILES_LOCATION

  ### Cloning and forking
<p>Forking a repository creates a copy of the original repository on GitHub account.
To fork a repository in GitHub:</p>
<ol>
<li>On GitHub.com, navigate to the repository.</li>
<li>In the top-right corner of the page, click Fork.</li>
<li>Select an owner for the forked repository.</li>
<li>By default, forks are named the same as their parent repositories. You can change the name of the fork to distinguish it further.</li>
<li>Optionally, add a description of your fork.</li>
<li>Choose whether to copy only the default branch or all branches to the new fork. For many forking scenarios, such as contributing to open-source projects, you only need to copy the default branch. By default, only the default branch is copied.</li>
<li>Click Create fork.</li>
</ol>

<p>Cloning a repository creates a copy of the original repository on our local machine.
To clone a repository in GitHub:</p>
<ol>
<li>On GitHub.com, navigate to your fork of the repository.</li>
<li>Above the list of files, click  Code.</li>
<li>Copy the URL for the repository.</li>
<ul>
    <li>To clone the repository using HTTPS, click the "Copy" icon on the right of "HTTPS".</li>
<li>To clone the repository using an SSH key, including a certificate issued by your organization's SSH certificate authority, click SSH, then click the icon on the right to copy it.</li>
  <li>To clone a repository using GitHub CLI, click GitHub CLI, then click the "Copy" icon on the right.</li>
</ul>
</ol>
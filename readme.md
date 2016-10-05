Sandbar Django Webapp Readme

## To get running locally:

In order to create a local development environment, you must have python 2.7 and virtualenv installed. The instructions below assume you are using Eclipse as your IDE. If you are using Eclipse, it's best if the PyDev plugin is installed as this allows you to use the PyDev perspective and declare the project as a Django project. I will try to point out Eclipse specific instructions. Also note, that it is easier to use a Linux system, but Windows is possible. You will need to modify the instructions which require command line interaction to there Windows equivalent. I'll try to note these changes.

### Step 1

Checkout the code from githup. If you are using Eclipse,  do the following:

1. Set up a python interpreter using your default python interpreter. This can be done from the Preferences  dialog under PyDev -> Interpreter - Python.
2. under PyDev, File -> import -> Git Projects from Git -> select project you want


### Step 2

Create your virtualenv. This should be in the sandbar directory. By convention, call it env. On linux systems you can use the following command from the command line after you have changed directories to sandbar:

```
% cd /where you but your workspace/sandbar
% virtualenv --python=python2.7 --no-site-packages env
```

* Note: You may get an error that "The executable python2.7 (from --python=python2.7) does not exist".  If this happens, delete the --python=python2.7 part and retry.

### Step 3

Install the project python requirements using pip. On linux you can do the following using the pip in the virtualenv. Alternatively, you can activate your environment and just use pip.

```
% env/bin/pip --timeout=120 install -r requirements.txt
```
* Note: In Windows, the command is env\scripts\pip --timeout=120 install -r requirements.txt

### Step 4

Set up your IDE to use the virtualenv you have just created. If you are using Eclipse, do the following.

1. Highlight the sandbar project, right click, and Refresh. You should see env directory appear
2. Go to Preferences and set up a new python interpretor using the one in the virtualenv that you just created. 3. On Macs/linux you may also need to set up a couple of environment variables (TNS_ADMIN and DYLD_LIBRARY_PATH)
4. Highlight the sandbar project, right click, and select Properties. Change the interpreter to use the one you just set up.
5. Highlight the sandbar project, right click, and select PyDev and Change to Django project.
6. Highlight the sandbar project, right click, and select Properties.In PyDev - Django, set manage.py to manage.py and Django settings module to sandbar_project.settings

### Step 5

Create a local_settings.py file in sandbar/sandbar_project (an example is there now).The local_settings.py is used for information such as passwords and the secret_key that shouldn't be committed to source control (there are no passwords in the example local_settings file, but once there are, it should not be committed to source control). You can set the secret_key to whatever is in the secret key on dev or really just anything for local development. The file can also be used for server specific settings. 

### Step 6

Test your installation by running the development server. In Eclipse do the following:

1. Highlight sandbar, right click, Run As --> PyDev Django. You should see no errors in the Console
2. In a browser, go to localhost:8000/home/ and you should see the home page.


*Note:* The first time you commit, you will want to add svn:ignore to local_settings.py, env, and any IDE specific dotfiles that were created. In Eclipse, these can be done from Team Synchronizing perspective.



## How the application is deployed at OWI, may not be applicable to your environment:

VMs:

* cida-eros-sbdjdev.er.usgs.gov
* cida-eros-sbdjqa.er.usgs.gov
* cida-eros-sbdjprod.er.usgs.gov

Databases:

* devdw.er.usgs.gov
* qadw.er.usgs.gov
* dbdw.er.usgs.gov

Schema owner is SANDBAR, application connects as SANDBAR_USER.

The application uses South, a django database management tool to create/maintain tables.

Jenkins:

* http://cida-eros-sbdjdev.er.usgs.gov:8080/jenkins/

* Build job: build_sandbar_django_webapp
* Deploy job: sandbar_webapp_deploy
* Sonar job: sandbar_webapp_sonar

Geoserver is NOT currently implemented in this application

Development URL:

http://cida-eros-sbdjdev.er.usgs.gov/wsgi/sandbar/surveys/sites/

Public QA URL:

http://cida-test.er.usgs.gov/gcmrc/sandbar/surveys/sites/

Production URL:

http://www.gcmrc.gov/sandbar/

Deployment directory structure:

```
webapps
|-- sandbar
|
wsgi
|-- sandbar
```

Build process (probably total overkill for your environment.  This basically zips up the directories and puts them into our nexus repository so that the deploy process can pull the zip file back down, copy it to the approprate application server and unzip it.  This can be done manually if necessary.):

```
source /etc/profile.d/oracle.sh;
cd sandbar;
virtualenv --no-site-packages --python=python2.7 env;
rm env/lib64;
ln -s lib env/lib64;
export PATH=$HOME/bin:$PATH:/usr/pgsql-9.3/bin;
echo $PATH;
export PIP_DOWNLOAD_CACHE="$HOME/.pip/download_cache/";
env/bin/pip --timeout=120 install -r requirements.txt;
echo "SECRET_KEY = 'key-for-jenkins'
POSTGIS_VERSION = (2, 1, 1)
SCHEMA_USER='djangotest'
DB_PWD='23test56'
DB_NAME='test_geodjango_db'" > sandbar_project/local_settings.py
yes yes | env/bin/python manage.py collectstatic;
export DBA_SQL_DJANGO_ENGINE=django.contrib.gis.db.backends.postgis 
export DBA_SQL_ADMIN=djangotest 
export DBA_SQL_DB_NAME=test_geodjango_db 
export DBA_SQL_ADMIN_PASSWORD=<password> 
export DBA_SQL_HOST=cida-eros-sbdjdev.er.usgs.gov 
export DBA_SQL_PORT=5432
export POSTGIS_VERSION=(2,1,1)
rm sandbar_project/local_settings.*;
if [ "$IS_M2RELEASEBUILD" = true ]; then
   git add env/* -f
   git add static/*
   git commit -a -m "automatic inclusion of the env and static files"
fi
```

Deployment process:

```
#reset workspace
rm -rf artifact
rm -f artifact.zip
#if script was called with a version number containing 'snapshot'
if grep -qi SNAPSHOT <<<$artifact_version; then
    REPOSITORY='cida-python-snapshots'
else
    REPOSITORY='cida-python-releases'
fi

#now that all parameters are set, retrieve the appropriate artifact from nexus

#A concise explanation how to leverage the Nexus REST API for our use case is found here: https://support.sonatype.com/entries/23674267-How-can-I-retrieve-a-snapshot-if-I-don-t-know-the-exact-filename-
#documentation for nexus rest api is found here: https://maven.java.net/nexus-core-documentation-plugin/core/docs/index.html

curl -v -u ${nexus_username}:${nexus_password} "https://internal.cida.usgs.gov/maven/service/local/artifact/maven/content?r=${REPOSITORY}&g=gov.usgs.cida.sandbar&a=sandbar_dj_webapp&c=zip&e=zip&v=${artifact_version}" > artifact.zip
#if file exists
if [ -s artifact.zip ]; then
    FILE_TYPE=`file -b --mime-type artifact.zip`
#if file type is correct
    if [ $FILE_TYPE = "application/zip" ]; then
        unzip artifact.zip -d artifact
        ls artifact
        echo "artifact successfully obtained"
        echo "creating symlink for local settings"
        cd artifact/*
        ln -s /opt/django/local/sandbar/local_settings.py sandbar_project/local_settings.py
        echo "creating symlink for sandbar_photos"
        ln -s /opt/django/.images/sandbar_photos static/sandbar_photos
        cd ../..
        echo "deploying..."
        rsync -avz --delete --exclude=artifact/local_settings.* --exclude=.git artifact/sandbar*/ django@${tier}:/opt/django/webapps/sandbar
        ssh django@${tier} 'sudo /sbin/service cida-httpd restart'
        echo "artifact successfully deployed"
    else
        echo "obtained something other than a zip file from nexus. Must obtain zip file"
        exit 1
    fi
else
    echo "ERROR: did not obtain file from nexus"
    exit 1
fi
```
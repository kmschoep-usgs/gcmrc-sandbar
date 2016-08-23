Sandbar Django Webapp Readme

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

Build process:

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
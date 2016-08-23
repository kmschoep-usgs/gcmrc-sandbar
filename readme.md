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

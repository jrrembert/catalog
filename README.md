# catalog

A simple flask app demonstrating hierarchal relationships between sports teams.

The site was tested in the most recent version of Chrome and no attempts were made to increase cross-browser capability. 

## Recommended Installation (using a Vagrant VM)

I recommend using the attached Vagrant configuration, however you can install [locally](#installlocal) as well. These instructions will assume you're using the VM and executing scripts from the VM's terminal (denoted where you see `vagrant-vm $` below).

Make sure that you have [VirtualBox](https://www.virtualbox.org/wiki/Download_Old_Builds) installed. **NOTE**: this project will not work on VirtualBox v5. The link directs you to v4.3 which is what I used for this project.

### From a terminal (OS X)

```
$ vagrant up default --provider=virtualbox
```

**Note**: You may see an error similar to:

```
The provider 'VirtualBox' could not be found, but was requested to
back the machine 'default'. Please use a provider that exists.
```

If you see this, look for a folder in your current working dir that looks like this: ```.vagrant/machines/<machine_name>/VirtualBox```. Simple change ```VirtualBox``` to virtualbox (or whatever spelling you provided to --provider) and the issue should be fixed.

### Initial setup (required)

1. Register an app at (https://console.developers.google.com).
2. Click on your newly-created project and go to "Credentials".
3. Click on "Download JSON".
4. Copy this file to your project root as ```client_secrets.json```
5. From a terminal (make sure you're within your project root):

  ```
  $ vagrant ssh
  $ cd /vagrant
  $ pip install -r requirements-vm.txt    ## May need to run as sudo
  $ python -c 'import database; database.init_db()'  ## Initialize db
  $ python run.py runserver   ### Run the app
  ```

6. Open a page to ```http://localhost:5001``` and go nuts.
7. Check out the [configuration](#configuration) and [test data](#testdata) sections for some additional steps you may want to take.








---


## <a id="installlocal"></a>OS X Installation (local)

### Initial setup (required)

1. Clone the repo
2. I highly recommend setting up a ```virtualenv``` before proceeding. You've been warned.
2. Register an app at (https://console.developers.google.com).
3. Click on your newly-created project and go to "Credentials".
4. Click on "Download JSON".
5. Copy this file to your project root as ```client_secrets.json```
6. From a terminal (make sure you're within your project root):

  ```
  $ pip install -r requirements-mac.txt    ## May need to run as sudo
  $ python -c 'import database; database.init_db()'  ## Initialize db
  $ python run.py runserver   ### Run the app
  ```

6. Open a page to ```http://localhost:5001``` and go nuts.
7. Check out the [configuration](#configuration) and [test data](#testdata) sections for some additional steps you may want to take.


---

### <a id="configuration"></a>Configuration (recommended)

The repo ships with two configuration files (located in ```/catalog_project```) named ```config.py``` and ```local_config_template.py```. ```config.py``` is the only config file used by the app and should contain any information you don't mind the public seeing. 

You will likely not want certain information exposed to the public (your secret key for instance). In this case, you will want to copy ```local_config_template.py``` as ```local_config.py``` and place any private information within this file. ```local_config.py``` is not checked by source control and any values in this config file will add or overwrite values in ```config.py```.

### <a id="testdata"></a>Test data (optional)

The repo ships with two helper scripts: ```teamdata.py``` and ```pave_db.sh```.

```teamdata.py``` contains some dummy data to prepopulate your db. Before running this script, you will need to set the value of ```USER_EMAIL``` within ```config.py``` or ```local_config.py``` equal to the gmail address you will use to log in to the site. Then simply run ```$ python teamdata.py``` to load some data into the database.

**Note: the following is for those using the VM**

For developers, the ```pave_db.sh``` script is available if you want to clear the db, reinitialize it, and populate it with data between builds. You will need to follow the instructions for ```teamdata.py``` above, then whenever you're ready to go, run ```$ ./pave_db.sh``` (you may need to run ```$ chmod +x pave_db.sh``` before proceeding.

### Migrations (optional)

Enable migrations if database exists (only need to do this once).
```
$ python run.py db init
```

Generate a migration (Alembic doesn't detect every change to model, indexes for instance, so these need to be double-checked).

```
$ python run.py db migrate
```

Apply migrations to database.
```
$ python run.py db upgrade
```

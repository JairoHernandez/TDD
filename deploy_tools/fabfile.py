from fabric.contrib.files import append, exists, sed
from fabric.network import ssh
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/JairoHernandez/TDD.git'
ssh.util.log_to_file("paramiko.log", 10)

def deploy():
	site_folder = '/home/%s/sites/%s' % (env.user, env.host) # env.host contains address of server, eg, superlists.jairomh.com. env.host is username used to log into server.
	source_folder = site_folder + '/source' 
	_create_directory_structure_if_necessary(site_folder)
	_get_latest_source(source_folder)
	_update_settings(source_folder, env.host)
	_update_virtualenv(source_folder)
	_update_static_files(source_folder)
	_update_database(source_folder)

def _create_directory_structure_if_necessary(site_folder):
	for subfolder in ('database', 'static', 'virtualenv', 'source'):
		run('mkdir -p %s/%s' % (site_folder, subfolder)) # 'run' is most common fabric command, which says "run this shell command on the server"

def _get_latest_source(source_folder):
	if exists(source_folder + '/.git'): # 'exists' checks whether a directory or file already exists on the server. We look for the 
										# .git hidden folder to check whether THe repo has already been cloned in that folder.
		run('cd %s && git fetch' % (source_folder,)) # Fabric does not have any state, it doesnt remember what directory you're in from one run to the next.
	else:
		run('git clone %s %s' % (REPO_URL, source_folder)) # Alternatively, we use git clone to bring down a fresh source tree.
	current_commit = local("git log -n 1 --format=%H", capture=True) # Fabric's 'local' command runs a command on your local machine__it's just a wrapper 
																	 # around subprocess.Popen really, but it's quite convenient. Here we capture the hash 
																	 # of the current commit that's in your local tree. That means the server will end up 
																	 # with whatever code is currently checked out on you machine(as long as you're pushed 
																	 # it up to the server)
	run('cd %s && git reset --hard %s' % (source_folder, current_commit)) #  We 'reset --hard' to that commit, which will blow away currnet changes in the server's code directory.

# NOTE: For this script to work, you  need to have a done a git push of your current local commit, so that the server can pull down and reset to it. If you see an 
# error saying 'Could not parse object', try doing a 'git push'.

# Update settings file, to set the 'ALLOWED_HOSTS' and 'DEBUG', and to create a new secret key:

def _update_settings(source_folder, site_name):
	settings_path = source_folder + '/superlists/settings.py'
	sed(settings_path, "DEBUG = True", "DEBUG = False") # String substitution of "DEBUG" from  True to False.
	sed(settings_path, 
		'ALLOWED_HOSTS = .+$',
		'ALLOWED_HOSTS = ["%s"]' % (site_name,) # Adjustting "ALLOWED_HOSTS", using a regex expression to match the right line.
	)
	secret_key_file = source_folder + '/superlists/secret_key.py'
	if not exists(secret_key_file): # Django uses "SECRET_KEY" for some of its crypto--cookies and CSRF protection. It's good practice to have the 
									# secret key on servers be different than the one in your(possibly public) source code repo.
		chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
		key = ''.join(random.SystemRandom().choice(chars) for _ in range (50))
		append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
	append(settings_path, '\nfrom .secret_key import SECRET_KEY') # Useing relative import "from .secret_key"  to be absolutely sure we're importing the local module. 
																  # Two scoops suggests using environment variables to set secret keys so use whatever is most comfortable.

# Next, create or update the virtualenv

def _update_virtualenv(source_folder):
	virtualenv_folder = source_folder + '/../virtualenv'
	if not exists(virtualenv_folder + '/bin/pip'): # Looking inside the virtualenv folder for pip executable to see if it already exists.
		run('virtualenv --python=python3 %s' % (virtualenv_folder,)) # 
	run('%s/bin/pip install -r %s/requirements.txt' % ( virtualenv_folder, source_folder )) #  found under /TDD/superlists

# Updating static files in a single command.

def _update_static_files(source_folder):
	run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput' % (source_folder,)) # Make sure to use the virtual environment Django version.

# Update database with manage.py migrate

def _update_database(source_folder):
	run('cd %s && ../virtualenv/bin/python3 manage.py migrate --noinput' % (source_folder,))



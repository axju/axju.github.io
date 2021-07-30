DevOps for blogging with Pelican
================================

:date: 2021-03-02 20:15
:category: devops
:tags: pelican, python, jenkins, devops
:summary: One (easy) way to automate your blogging with Pelican and Jenkins.


Today I will show you my blogging setup and workflow. A few years ago I build a
blog with `Flask <https://flask.palletsprojects.com/en/1.1.x/>`__. But this wars
more a project to learn `Python <https://www.python.org>`__. I like to share
my coding experience, but maintaining a self build blog software wars more pain
then fun. So I switch to `WordPress <https://wordpress.com/>`__. And yes,
that `works fine <https://www.short-report.de/>`__.

To be honest, I don't like `WordPress <https://wordpress.com/>`__. It has to be
good software, but I don't like writing in the cloud. I like to have my post as
a plain text on my local device. I write some tools to make that work. But
again, I would share my experience as a developer and not maintain some nasty
projects.

It was also the time when we renovated our house and had children shortly
afterwards. So I had less time to look after my blog. Now as they get older, I
have more time for this. And my DevOps skills have also increased. I setup a
`Jenkins server <{filename}/articles/devops/001-jenkins-on-raspberry-pi.rst>`__
and play with it, just for fun. And then I discovered
`Pelican <https://docs.getpelican.com/en/3.6.3/index.html>`__, as static page
generator. This would change my blogging workflow to the following:

1. I write the content(rst files) on my locale device.
2. With Pelican I create the HTML files and look at the preview blog.
3. If I'm happy with the result, I push them to a git repository.
4. The Jenkins server build the finale blog and publish it.

And that's it. I just want to share how my blogging workflow look. If you are
interesting in the technical details, go on. Otherwise have a nice day.

Some details
------------
The git repository has a *Jenkinsfile*, which will be read from the Jenkins
server. When I commit my changes to the repository, a webhook triggers the build
process on the server.

To publish the blog I installed the plugin *Publish Over SSH* on the Jenkins
server. With this I can copy the HTML files to the web server. You can have
several configuration files for your
`Pelican <https://docs.getpelican.com/en/3.6.3/index.html>`__ project. I have
one for development, one for the web server and one for a hidden service. The
web server build is only executed in the main branch. So the onion version of my
blog is always a little newer.

Jenkinsfile
-----------
.. code-block:: bash

  pipeline {
    agent {
      docker {
        image 'python:3.8'
      }
    }
    stages {
      stage('setup') {
        steps {
          withEnv(["HOME=${env.WORKSPACE}"]) {
            sh 'python -m pip install --user --upgrade pip pelican'
            sh 'python --version'
            sh 'python -m pelican --version'
          }
        }
      }

      stage('publish - web') {
        when {
          branch 'master'
        }
        steps {
          withEnv(["HOME=${env.WORKSPACE}"]) {
            sh 'python -m pelican content -s publishconf.py'
          }
          sshPublisher(
            publishers: [
              sshPublisherDesc(
                configName: 'web-projects',
                sshRetry: [retries: 5, retryDelay: 10000],
                transfers: [
                  sshTransfer(
                    remoteDirectory: 'axju',
                    removePrefix: 'output/',
                    sourceFiles: 'output/**/*'
                  )
                ]
              )
            ]
          )
        }
      }

      stage('publish - onion') {
        steps {
          withEnv(["HOME=${env.WORKSPACE}"]) {
            sh 'python -m pelican content -s raspiconf.py'
          }
          sshPublisher(
            publishers: [
              sshPublisherDesc(
                configName: 'onion-projects',
                sshRetry: [retries: 5, retryDelay: 10000],
                transfers: [
                  sshTransfer(
                    remoteDirectory: 'axju',
                    removePrefix: 'output/',
                    sourceFiles: 'output/**/*'
                  )
                ]
              )
            ]
          )
        }
      }


    }
    post {
      always {
        cleanWs()
      }
    }
  }

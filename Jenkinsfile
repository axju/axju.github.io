pipeline {
  agent {
    docker {
      label 'dragon'
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
    stage('build') {
      steps {
        withEnv(["HOME=${env.WORKSPACE}"]) {
          sh 'python -m pelican content -s publishconf.py'
        }
      }
    }
    stage('publish - netcup') {
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
              configName: 'netcup-projects',
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

    stage('publish - netcup dev') {
      steps {
        withEnv(["HOME=${env.WORKSPACE}"]) {
          sh 'python -m pelican content -s publishconf.py'
        }
        sshPublisher(
          publishers: [
            sshPublisherDesc(
              configName: 'netcup-projects',
              sshRetry: [retries: 5, retryDelay: 10000],
              transfers: [
                sshTransfer(
                  remoteDirectory: 'dev',
                  removePrefix: 'output/',
                  sourceFiles: 'output/**/*'
                )
              ]
            )
          ]
        )
      }
    }

    stage('publish - raspberrypi') {
      steps {
        withEnv(["HOME=${env.WORKSPACE}"]) {
          sh 'python -m pelican content -s raspiconf.py'
        }
        sshPublisher(
          publishers: [
            sshPublisherDesc(
              configName: 'raspberrypi',
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

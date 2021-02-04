pipeline {
  agent {
    docker {
      image 'python:3.8'
    }
  }
  stages {
    stage('setup') {
      steps {
        sh 'python -m pip install --upgrade pip pelican'
        sh 'python --version'
        sh 'python -m pelican --version'
      }
    }
    stage('build') {
      steps {
        sh 'python -m pelican content -s publishconf.py'
      }
    }
    stage('build') {
      when {
        branch 'master'
      }
      steps {
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
  }
  post {
    always {
      cleanWs()
    }
  }
}

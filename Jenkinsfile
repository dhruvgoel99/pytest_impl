
pipeline {
  agent any
  stages {
    stage('install') {
      steps {
        sh 'sudo apt install python3'
      }
    }
    stage('requirements and report') {
      steps {
        sh 'pip3 install -r requirements.txt'
        sh 'pytest -v -m cli'
        sh 'pytest --html=report.html'
      }
    }
  }
}

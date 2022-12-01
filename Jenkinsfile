
pipeline {
  agent any
  stages {
    stage('build') {
      agent {
                docker {
                    image 'python:2-alpine'
                }
            }
            steps {
                sh 'python -m py_compile sources/add2vals.py sources/calc.py'
                stash(name: 'compiled-results', includes: 'sources/*.py*')
            }
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

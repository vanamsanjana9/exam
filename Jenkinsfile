
pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                echo "Running tests"
                bat 'pip install -r requirements.txt'
                bat 'start /B python app.py'
                bat 'ping 127.0.0.1 -n 5 > nul'
                bat 'pytest -v'
            }
        }

        stage('Build') {
            steps {
                echo "Building Docker Image"
                bat 'docker build -t kubedemoapp:v1 .'
            }
        }

        stage('Docker Login') {
            steps {
                echo "Docker Login"
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKERHUB_USER',
                    passwordVariable: 'DOCKERHUB_TOKEN'
                )]) {
                    bat 'echo %DOCKERHUB_TOKEN% | docker login -u %DOCKERHUB_USER% --password-stdin'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                echo "Pushing Docker Image"
                bat 'docker tag kubedemoapp:v1 vanamsanjana9/sample:seleniumtest'
                bat 'docker push vanamsanjana9/sample:seleniumtest'
            }
        }

        stage('Deploy') {
            steps {
                bat 'kubectl apply -f deployment.yaml --validate=false'
                bat 'kubectl apply -f service.yaml'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}

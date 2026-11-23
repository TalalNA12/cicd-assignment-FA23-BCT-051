pipeline {
    agent any

    environment {
        IMAGE_NAME = 'talal-cicd-site'
        STAGING_PORT = '8090'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Validating website files'
                sh 'test -f src/index.html'
                sh 'grep -q "FA23-BCT-051" src/index.html'
            }
        }

        stage('Package') {
            steps {
                echo 'Building website Docker image'
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
            }
        }

        stage('Start Staging') {
            steps {
                echo 'Starting staging website'
                sh '''
                    docker rm -f talal-staging || true
                    docker run -d --name talal-staging \
                        -p 8090:80 \
                        ${IMAGE_NAME}:${BUILD_NUMBER}

                    sleep 3
                    curl -sf http://localhost:8090/ > /dev/null
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running Selenium tests inside Docker'
                sh '''
                    docker run --rm --network host \
                        -u $(id -u):$(id -g) \
                        -e HOME=/tmp \
                        -e BASE_URL=http://localhost:8090 \
                        -v "$WORKSPACE":/work \
                        -w /work \
                        selenium-test-agent \
                        pytest tests/test_site.py -v \
                        --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                    archiveArtifacts artifacts: 'screenshot.png', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'All tests passed. Deploying to production'
                sh '''
                    docker rm -f talal-production || true
                    docker run -d \
                        --name talal-production \
                        --restart unless-stopped \
                        -p 80:80 \
                        ${IMAGE_NAME}:${BUILD_NUMBER}
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f talal-staging || true'
        }
        success {
            echo 'CI/CD pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Deployment was skipped if tests failed.'
        }
    }
}

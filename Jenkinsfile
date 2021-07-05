pipeline {
    agent {
        label 'agent-python'
    }

    stages {
        stage('Activate virtual environment') {
            steps {
                sh "virtualenv venv"
                sh ". venv/bin/activate"
            }
        }
        stage('Install Python dependencies') {
            steps {
                sh "pip install -r requirements.txt"
            }
        }
        stage('PEP8 (Flake)') {
            steps {
                sh "doit flake"
            }
            post {
                always {
                    recordIssues(
                        sourceCodeEncoding: 'UTF-8',
                        sourceDirectory: 'src/',
                        enabledForFailure: true,
                        tool: flake8(pattern: 'reports/*.txt'),
                        qualityGates: [
                            [threshold: 5, type: 'TOTAL', unstable: true],
                            [threshold: 10, type: 'TOTAL', unstable: false]
                        ]
                    )

                }
            }
        }
    }
}
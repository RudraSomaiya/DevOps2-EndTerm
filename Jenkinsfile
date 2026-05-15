pipeline {
    agent any
 
    environment {
        APP_PORT = "5000"
    }
 
    stages {
 
        stage("Checkout") {
            steps {
                echo "=== Cloning repository from GitHub ==="
                git branch: "main",
                    url: "https://github.com/RudraSomaiya/DevOps2-EndTerm.git"
            }
        }
 
        stage("Build") {
            steps {
                echo "=== Installing Python dependencies ==="
                sh "sudo pip3 install -r requirements.txt --quiet --break-system-packages"
                echo "Build completed successfully."
            }
        }
 
        stage("Test") {
            steps {
                echo "=== Running unit tests with pytest ==="
                sh "python3 -m pytest test_app.py -v --tb=short"
                echo "All tests passed."
            }
        }
 
        stage("Deploy") {
            steps {
                echo "=== Deploying Flask application ==="
                sh """
                    # Kill any existing Flask process
                    pkill -f "python3 app.py" 2>/dev/null || echo "No existing process"
                    sleep 2
 
                    # Deploy: run Flask in background from Jenkins workspace
                    nohup python3 app.py > /tmp/flask_app.log 2>&1 &
                    sleep 4
 
                    # Health check
                    if pgrep -f "python3 app.py" > /dev/null; then
                        echo "SUCCESS: Flask app running on port 5000"
                    else
                        echo "FAILURE: App did not start. Check /tmp/flask_app.log"
                        exit 1
                    fi
                """
            }
        }
    }
 
    post {
        success {
            echo "PIPELINE SUCCESS: Application deployed at http://EC2_IP:5000"
        }
        failure {
            echo "PIPELINE FAILED: Check the stage logs above for errors."
        }
        always {
            echo "Pipeline finished at ${new Date()}"
        }
    }
}

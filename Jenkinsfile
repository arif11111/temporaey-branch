pipeline {
	agent any

        environment {
	DOCKER_REG = 'a5edevopstuts' 
        IMAGE_NAME_1 = 'webserver-1' 
        IMAGE_NAME_2 = 'webserver-2' 
        DOCKER_ID = "${DOCKER_REG}/${IMAGE_NAME}"  // container ID for running the docker image locally    
    }

    stages {
               
        stage('Git checkout') {
            steps {
                script{                
                    checkout scm
                }
            }           
        }
               
        stage('Docker Build and Push') {
        	agent any
            steps {
               withCredentials([usernamePassword(credentialsId: 'cf193cec-8eb9-4aee-9e8b-9ab9bcf38c84', passwordVariable: 'docker_passwd', usernameVariable: 'docker_usrname')]) {
    
                    sh """
                    cd Webserver-1
                    docker build -t ${DOCKER_REG}/${IMAGE_NAME_1}:${BUILD_NUMBER} .
		    docker login -u $\{docker_usrname\} -p $\{docker_passwd\}
                    docker push ${DOCKER_REG}/${IMAGE_NAME_1}:${BUILD_NUMBER}
                    WEBSERVER1_DOCKER_ID=${DOCKER_REG}/${IMAGE_NAME_1}:${BUILD_NUMBER}
        
                    cd ../Webserver-2
                    docker build -t ${DOCKER_REG}/${IMAGE_NAME_2}:${BUILD_NUMBER} .
                    docker push ${DOCKER_REG}/${IMAGE_NAME_2}:${BUILD_NUMBER}
                    WEBSERVER2_DOCKER_ID=${DOCKER_REG}/${IMAGE_NAME_2}:${BUILD_NUMBER}"""
        
                }
            }
        }
   }
}

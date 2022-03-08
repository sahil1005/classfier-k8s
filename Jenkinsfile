pipeline {
    agent any
	
	environment {
		PROJECT_ID = 'ppedetonline'
                CLUSTER_NAME = 'ppedetonline-cluster'
                LOCATION = 'asia-south1-a'
                CREDENTIALS_ID = 'kubernetes'
						
	}
	
    stages {
	    stage('Scm Checkout') {
		    steps {
			    checkout scm
		    }
	    }
	    
	    stage('Build Docker Image modelserver') {
		    steps {
				sh 'whoami'
			    script {
					myimage = docker.build("asia.gcr.io/ppedetonline/modelserver:${env.BUILD_ID}", "./modelserver") 
					} 
				}
	    }

		stage("Pushing modelserver image to gcr.io") {
		    steps {
			    script {
				   withCredentials([file(credentialsId: 'gcr', variable: 'GC_KEY')]){
              sh "cat '$GC_KEY' | docker login -u _json_key --password-stdin https://asia.gcr.io"
              sh "gcloud auth activate-service-account --key-file='$GC_KEY'"
              sh "gcloud auth configure-docker"
              GLOUD_AUTH = sh (
                    script: 'gcloud auth print-access-token',
                    returnStdout: true
                ).trim()
              echo "Pushing image To GCR"
              sh "docker push asia.gcr.io/ppedetonline/modelserver:${env.BUILD_ID}"
          			}  
			    }
		    }
	    }



		stage('Build Docker Image webserver') {
		    steps {
				sh 'whoami'
			    script {
						myimage = docker.build("asia.gcr.io/ppedetonline/webserver:${env.BUILD_ID}", "./webserver") 
					} 
				}
	    }

		stage("Pushing webserver image to gcr.io") {
		    steps {
			    script {
				   withCredentials([file(credentialsId: 'gcr', variable: 'GC_KEY')]){
              sh "cat '$GC_KEY' | docker login -u _json_key --password-stdin https://asia.gcr.io"
              sh "gcloud auth activate-service-account --key-file='$GC_KEY'"
              sh "gcloud auth configure-docker"
              GLOUD_AUTH = sh (
                    script: 'gcloud auth print-access-token',
                    returnStdout: true
                ).trim()
              echo "Pushing image To GCR"
              sh "docker push asia.gcr.io/ppedetonline/webserver:${env.BUILD_ID}"
          			}  
			    }
		    }
	    }


	    
	    stage('Deploy to K8s') {
		    steps{
			    echo "Deployment started ..."
			    sh 'ls -ltr'
			    sh 'pwd'
			    sh "sed -i 's/tagversion/${env.BUILD_ID}/g' modelserver.yaml"
				sh "sed -i 's/tagversion/${env.BUILD_ID}/g' webserver.yaml"
				echo "Start deployment of app-env-configmap.yaml"
			    step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: 'app-env-configmap.yaml', credentialsId: env.CREDENTIALS_ID, verifyDeployments: true])
			    echo "Start deployment of modelserver.yaml"
			    step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: 'modelserver.yaml', credentialsId: env.CREDENTIALS_ID, verifyDeployments: true])
				echo "Start deployment of webserver.yaml"
				step([$class: 'KubernetesEngineBuilder', projectId: env.PROJECT_ID, clusterName: env.CLUSTER_NAME, location: env.LOCATION, manifestPattern: 'webserver.yaml', credentialsId: env.CREDENTIALS_ID, verifyDeployments: true])
			    echo "Deployment Finished ..."
		    }
	    }
    }
}

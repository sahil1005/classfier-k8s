pipeline {
    agent any
	
	environment {
		PROJECT_ID = 'qwiklabs-gcp-01-770f8f7f5c74'
                CLUSTER_NAME = 'k8s-cluster'
                LOCATION = 'us-central1-c'
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
			    sh "docker build -t hellcasterexe/modelserver:${env.BUILD_ID} ./modelserver"
				}
	    }

		stage('Build Docker Image webserver') {
		    steps {
			    sh "docker build -t hellcasterexe/weblserver:${env.BUILD_ID} ./webserver"
				}
	    }
	    
	    stage("Push Docker Image") {
		    steps {
			    script {
				    echo "Push Docker Image"
				    withCredentials([string(credentialsId: 'dockerhub', variable: 'dockerhub')]) {
            				sh "docker login -u hellcasterexe -p ${dockerhub}"
				    }
				        myimage.push("${env.BUILD_ID}")
				    
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

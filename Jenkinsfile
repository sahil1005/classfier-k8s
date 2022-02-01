pipeline {
    agent any
	
	environment {
		PROJECT_ID = 'qwiklabs-gcp-00-10c2f43b64a0'
                CLUSTER_NAME = 'classifier-project'
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
				sh 'whoami'
			    script {
					myimage = docker.build("hellcasterexe/modelserver:${env.BUILD_ID} ./modelserver")

					} 
				}
	    }

		stage('Build Docker Image webserver') {
		    steps {
				sh 'whoami'
			    script {
					myimage = docker.build("hellcasterexe/webserver:${env.BUILD_ID} ./webserver")
					
					} 
				}
	    }
	    
	    stage("Docker Login") {
		    steps {
			    script {
				    echo "Docker Login"
				    withCredentials([string(credentialsId: 'dockerhub', variable: 'dockerhub')]) {
            				sh "docker login -u hellcasterexe -p ${dockerhub}"
				    }  
			    }
		    }
	    }

		stage("Docker push image modelserver") {
			steps {
				script {
					myimage.push("hellcasterexe/modelserver${env.BUILD_ID}")
				}
			}

		}

		stage("Docker push image webserver") {
			steps {
				script {
					myimage.push("hellcasterexe/webserver${env.BUILD_ID}")
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

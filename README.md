# Static Web Pages Application Hosting

This project features a static webpages application deployed as workloads on AWS Managed EKS cluster.
The static web application consists of two web pages hosted on its particular nginx webserver which is authenticated through users credentials.

Tools been utilized for the process - </br>
**[Nginx Webserver]** - Using Nginx configurations defined to host the index page on the nginx alpine base image. </br>

**[Docker]** - Which is used to build and publish image to the Docker Hub Repository. </br>

**[Jenkins]** - As an automation pipeline to build the images, publish it on the dockerhub repo and update the build instance image name in helm chart. </br>

**[Terraform]** - For spinning up EKS cluster and corresponding the supporting VPC modules in AWS. </br>

**[EKS]** - RUnning on us-west-2 region.</br>

**[Helm Charts]** - This bascially bundles or package up the resource needed for building up the application. It also basically links the kubernetes objects which has been deployed for the kubernetes cluster.</br>

**[ArgoCD]** - A tool for automating helm charts deployment on K8s cluster.

<h3> Creating AWS VPC and EKS cluster </h3>

**Provide AWS Credentials**

```
$ aws configure:
$............... AWS Access Key ID [None]:
$............... AWS Secret Access Key [None]:
$............... Default region name [None]:
$............... Default output format [None]:
```

Initialize and pull terraform cloud specific dependencies:
```
$ terraform init
```
View terraform plan:
```
$ terraform plan
```
Apply terraform plan:
```
$ terraform apply
```

Terraform modules will create
```
-   VPC
-   Subnets
-   Routes
-   IAM Roles for master and nodes
-   Security Groups "Firewall" to allow master and nodes to communicate
-   EKS cluster
-   Managed nodes groups to be added to the cluster
```

Executing the command will prompt the kubeconfig file to be loaded within your home .kube directory
```
aws eks --region us-west-2 update-kubeconfig --name my-cluster
```
<h2> Nginx Webserver Configuration </h2> 
The nginx configuration consists of a basic method to host the static page on default server on port 80.

<h2> Jenkins CI/CD for creating webservers docker image </h2> 

The Jenkins file will clone the repo and create docker images with the version being the Job Build instance ```${DOCKER_REG}/${IMAGE_NAME}:${BUILD_NUMBER}``` and will publish into the docker hub repo and will update the job instance build image name into values.yaml helm chart.

<img width="317" alt="Jenkins-image-creation-1" src="https://user-images.githubusercontent.com/33144027/203221915-92a91c50-9a99-4d81-a8df-933ef27de2a7.PNG">
<img width="382" alt="Jenkins-image-creation-2" src="https://user-images.githubusercontent.com/33144027/203222292-6440ef8f-b71d-4d41-bf24-1b8bbfec0afa.PNG">

<h2> Installation in Kubernetes cluster </h2>

Before begining with the applicaton  deployments, there are some pre-requisites to be installed within the deployment.

**Nginx-Ingress** - To allow path base routing to our web pages. </br>
```https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.1.1/deploy/static/provider/cloud/deploy.yaml``` </br>

<img width="943" alt="ingress-nginx" src="https://user-images.githubusercontent.com/33144027/203225933-c28aee31-33ba-4332-8537-c8650b62ed09.PNG"> </br>
The ingress controller service will be assigned a AWS Load Balancer automatically which will be our Hostname to route to our webservers static pages.

**Metrics-Server** - To monitor the metrics on the application workload for load testing. </br>
```kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml``` </br>
<img width="658" alt="metrics-endpoint" src="https://user-images.githubusercontent.com/33144027/203225806-a796aac3-fa3b-4b7f-90ae-2cc87aca8f66.PNG"> </br>
This verifies that metrics API is running properly within our cluster.

**ArgoCD** - For Automated Deployment of manifests/helm chart in Kubernetes Cluster. </br>
```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

<h3> Kubernetes Application Resources </h3>
THe webserver application workload consists of the following  kubernetes objects - 
1. Deployment</br>
2. Service</br>
3. Ingress Resource</br>
4. Horizontal Pod Autoscaler</br>

Also, to make our web pages user authenticated we make use of secrets to pass those credentials within our ingress resources - 
```
kubectl create secret generic basic-auth --from-file=auth
```
where the auth file contains password created from htpassword module and that secret will be used within annotations in our ingress resource to allow the webservers to be authenticated. </br>
<img width="374" alt="secret" src="https://user-images.githubusercontent.com/33144027/203225730-1d27832e-2101-42de-ad65-903e347ff72e.PNG"> </br>


<h2> Application resource deployments in Kubernetes cluster </h2>

Our current repository is configured within argocd and then the two webservers directory path ```webserver-1/helm``` and ```webserver-2/helm``` is mentioned within the ArgoCD applications creation which initiates in the deployment of our applications resources within the cluster. </br>
**Webserver-1 Application Workloads** -

<img width="776" alt="web-server-1-argocd" src="https://user-images.githubusercontent.com/33144027/203227414-9f9fab2c-7d65-43ce-9702-5180edd36f3c.PNG">

<img width="857" alt="web-server-1 workloads" src="https://user-images.githubusercontent.com/33144027/203227448-8e1e50b1-c22d-476d-bc9f-713f80ff11eb.PNG"> </br>

**Webserver-2 Application Workloads** -

<img width="772" alt="web-server-2-argocd" src="https://user-images.githubusercontent.com/33144027/203227700-589a581c-8ed9-435e-80da-782a60997940.PNG">

<img width="832" alt="web-server-2 workloads" src="https://user-images.githubusercontent.com/33144027/203227708-7288b63c-19a7-4fa9-9fdf-021869dd26e7.PNG"> </br>


**Ingress Resource** - This consists of the ingress path base routing to different web pages with secrets configured within the annotation.</br>
<img width="711" alt="webserver-ingress" src="https://user-images.githubusercontent.com/33144027/203232170-a02ca178-e91f-475a-8f63-f9751dfc9920.PNG">

where ```<dns-hostname>/stats-1``` route to the first page whereas ```<dns-hostname>/stats-2``` route to the second page of the application.

Final Results - 

<img width="623" alt="Page-1-auth" src="https://user-images.githubusercontent.com/33144027/203232703-6c0c5c10-242b-4be9-ad8e-f5f2739398d6.PNG">
<img width="645" alt="Page-1" src="https://user-images.githubusercontent.com/33144027/203232752-ac1a11c1-03cc-45d6-ac54-7cddc79631a8.PNG">
<img width="662" alt="Page-2" src="https://user-images.githubusercontent.com/33144027/203232777-df5f397c-3435-4264-bbe1-b64bf7fa6b50.PNG">

**Load Testing** - As a way to measure of how our webserver reacts in accordance to the traffic load occurs, we can make use of Horizontal Pod autoscaler with metrics pointing to the CPU utilization and will generate a new replica pod as soon as the threshold will reached.

```kubectl apply -f load-testing-deployment.yaml``` </br>
This deployment will generate a traffic to the application pods by continuously accessing the page of the application.

The traffic load can be measured by viewing the pod autoscaler in the cluster.
<img width="712" alt="hpa-w" src="https://user-images.githubusercontent.com/33144027/203240123-3c8b6c2a-6598-4c91-b323-3129f6ba89b3.PNG"></br>

As soon as the load threshold increases, we see the new replica gets created to match the max no. of pods replica.
<img width="522" alt="autoscale-web-server-1" src="https://user-images.githubusercontent.com/33144027/203240284-b641d949-06bc-4262-a2ea-f119e251b91e.PNG">

<img width="629" alt="autoscale-web-server-2" src="https://user-images.githubusercontent.com/33144027/203240293-2ff8bf30-095a-4887-a105-4eed3a6f4707.PNG">




<h2> Webserver Hosting as Workload Approach Insights </h2>

**The current approach involves**: 
- creating a docker image particularly for each web server with its hosting index page. This helps us in maintiaing the code template which can be shipped into different environments Machines with different configurations as our Image will be running in isolated environment
- Creating Helm Chart for each webserver and its docker image id getting updated with the latest image id with python script and that can be automated with a CI tool (Jenkins). Due to this, the Image creation instance is always unique and the same created image is been deployed into cluster without any human intervention to deploy the latest config.
- Creation of EKS Cluster and its corresponding AWS resources involved with an IAC tool - Terraform. Provisioning Infra with a IAC tool helps in managing the resources in bunch of code due to which it can be extensible, re-writable and re-usable in creating mutliple setups of the same structure.
- The static page docker images are then deployed as workload in kubernetes cluster in multi-replicas mode. Deploying our workloads into multiple pods allows to have Highly - available/scalable architecture. 
- Usage of ArgoCD for deploying the helm charts onto kubernetes cluster with GitOps principles so that every image is automatically reflected in the cluster. GItOps principles helps in maintaining the state of our cluster according to our requirements and compatibility.
- The Deployments are then accessible through ingress path routing method with authentication enabled using secrets. Ingress in a K8s Cluster allows to make use of Load balancing the request which helps in processing the traffic request faster and easier. Also, authentication can also be managed either using Credentials or SSL/TLS encryption of the website needed.
- Load Testing involves Horizontal Pod Autoscaler which can scale the no of application workloads according to our requirement till the traffic is under threshold. 











https://medium.com/avmconsulting-blog/running-a-python-application-on-kubernetes-aws-56609e7cd88c

Running a Python Application on Kubernetes

Kubernetes is an open-source container-orchestration system for automating computer application deployment, scaling, and management. It was originally designed by Google and is now maintained by the Cloud Native Computing Foundation.

Whether you would like to run a straightforward Python application or a fancy one, Kubernetes will quickly and expeditiously assist you to deploy and scale your applications, seamlessly roll out new options whereas limiting resources to only needed resources.

In this article, I will be able to discuss a holistic method of deploying a straightforward Python application to Kubernetes

You will see the below topic included in the article :

    You will see we will be creating Python container images
    After the creation of images, we will work on publishing the container images to an image registry
    Once published to registry we will create and work with Persistent Volume
    Least but not last, then we will be deploying the Python application to the Kubernetes cluster

PreRequisites:

You will be needing the following to start with the lab:

    Docker

Docker is an open platform to build and ship distributed applications. To install Docker on Debian/Ubuntu:

sudo apt-get install docker.io

Let's verify that Docker is running properly, Shoot the command docker info

$ docker info
Containers: 0
Images: 289
Storage Driver: aufs
 Root Dir: /var/lib/docker/aufs
 Dirs: 289
Execution Driver: native-0.2
Kernel Version: 3.16.0–4-amd64
Operating System: Debian GNU/Linux 8 (jessie)
WARNING: No memory limit support
WARNING: No swap limit support

    kubectl

kubectl is a command-line interface for executing commands against a Kubernetes cluster. You will now play the script(shell) in order to install the kubectl component.

install_kubectl.shcurl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl

Let's take a look over Containerization

Containerization involves packing an application with its own software package. using dockerizing container rather than full machine virtualization gives the advantage of having the ability to run an application on any machine without worrying about its dependencies. We’ll begin with provisioning an image of the container for our Python demo code.
Let’s focus on Python Container Image

To provision the images we will be using the technology Docker, It's a great and unique solution that helps us to deploy the apps within isolated LXC.

Docker is able to automatically build images using instructions from a Docker file, such as the following for our Python application:

FROM python:3.6
MAINTAINER XenonStack
 
# Creating Application Source Code Directory
RUN mkdir -p /k8s_python_demo_code/src# Setting Home Directory for containers
WORKDIR /k8s_python_demo_code/src# Installing python dependencies
COPY requirements.txt /k8s_python_demo_code/src
RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install — no-cache-dir -r requirements.txt# Copying src code to Container

RUN pip install   -r requirements.txt# Copying src code to Container
COPY . /k8s_python_demo_code/src/app# Application Environment varia
ENV APP_ENV development# Exposing Ports
EXPOSE 4025# Setting Persistent data
VOLUME [“/app-data”]# Running Python Application
CMD [“python”, “app.py”]








docker create -ti --name dummy caijie/k8s_python_data_process:0.1


This Docker file contains instructions to run our DEMO Python code, It uses Python 3.5 Version to operate. We can now build the Docker image from these instructions using this command:

docker build -t k8s_python_data_process .

This command creates a Docker image for our Python application.
Publishing the Container Images to Registry

We can publish our Python image to completely different private/public cloud repositories like Dockerhub, AWS ECR, etc. We will be using Dockerhub for this lab.

We need to be careful that before we publish the image, we need to tag it to a specific version.

docker tag k8s_python_data_process:latest k8s_python_data_process:0.1

So once we are done with tagging and image with a specific version, Let's now push the image to the Dockerhub to store the image.

Shoot the Docker command to push the image.

docker push caijie73/k8s_python_data_process

Working with Persistent Storage in k8s

Kubernetes widely supports persistent storage solutions, such as NFS, Azure Disk, AWS EBC, CephFS, etc. We will be using Kubernetes' persistent storage with CephFS here.

In order to use CephFS for persistent data to Kubernetes containers, we will be creating two sets of files:

    persistent-volume.yml

apiVersion: v1
kind: PersistentVolume
metadata:
 name: app-disk01
 namespace: k8s_python_demo_code
spec:
 capacity:
 storage: 100Gi
 accessModes:
 — ReadWriteMany
 cephfs:
 monitors:
 — “172.16.0.1:2345”
 user: admin
 secretRef:
 name: ceph-secret
 readOnly: false

    persistent_volume_claim.yaml

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
 name: appclaim01
 namespace: k8s_python_demo_code
spec:
 accessModes:
 — ReadWriteMany
 resources:
 requests:
 storage: 20Gi

We can now use kubectl to add the persistent volume and claim to the Kubernetes cluster.

$ kubectl create -f persistent-volume.yml
$ kubectl create -f persistent-volume-claim.yml

Hopefully, after all the conditions fulfilled we are now good to deploy the application to K8s.
Deploying the Application to Kubernetes cluster

To manage our last mile of deploying the application to Kubernetes, we will create two important files:

    Service file

Create a file and name it “k8s_python_demo_code.service.yml” with the following content.

apiVersion: v1
kind: Service
metadata:
 labels:
 k8s-app: k8s_python_demo_code
 name: k8s_python_demo_code
 namespace: k8s_python_demo_code
spec:
 type: NodePort
 ports:
 — port: 4025
 selector:
 k8s-app: k8s_python_demo_code

    Deployment file

Create a file and name it “k8s_python_demo_code.deployment.yml” with the following content.

apiVersion: extensions/v1beta1
kind: Deployment
metadata:
 name: k8s_python_demo_code
 namespace: k8s_python_demo_code
spec:
 replicas: 2
 template:
 metadata:
 labels:
 k8s-app: k8s_python_demo_code
 spec:
 containers:
 — name: k8s_python_demo_code
 image: k8s_python_demo_code:0.1
 imagePullPolicy: “IfNotPresent”
 ports:
 — containerPort: 4025
 volumeMounts:
 — mountPath: /app-data
 name: k8s_python_demo_code
 volumes:
 — name: < application name >
 persistentVolumeClaim:
 claimName: appclaim01

Finally, use kubectl to deploy the application to Kubernetes:

$ kubectl create -f k8s_python_demo_code.deployment.yml $ kubectl create -f k8s_python_demo_code.service.yml

Congratulations, your application was successfully deployed to Kubernetes.

Lets now also confirm if your app is perfectly running by shooting a command

kubectl get services



https://martinheinz.dev/blog/20


Deploy Any Python Project to Kubernetes
MartinApr 15, 2020
DevOpsPythonKubernetes

As your project grows, it might get to the point that it becomes too hard to handle with just single VM or some simple SaaS solution. You can solve that by switching to more robust solution like Kubernetes. That might however, be little too complex if you are not familiar with it's concepts or if just never used it before. So, to help you out - in this article - we will go over all you need to get yourself started and have your Python project deployed on cluster - including cluster setup, all the Kubernetes manifests and some extra automation to make your life easier down the road!

This is a follow up to previous article(s) about Automating Every Aspect of Your Python Project, so you might want check that out before reading this one.

TL;DR: Here is my repository with full source code and docs: https://github.com/MartinHeinz/python-project-blueprint
Comfy Development Setup

To be productive in your development process, you need to have comfy local development setup. Which in this case means having simple to use Kubernetes on local, closely mirroring your real, production cluster and for that, we will use KinD:

KinD (Kubernetes-in-Docker), as the name implies, runs Kubernetes clusters in Docker containers. It is the official tool used by Kubernetes maintainers for Kubernetes v1.11+ conformance testing. It supports multi-node clusters as well as HA clusters. Because it runs K8s in Docker, KinD can run on Windows, Mac, and Linux. So, you can run it anywhere, you just need Docker installed.

So, let's install KinD (on Linux - if you are on Windows, see installation info here):

~ $ curl -Lo ./kind https://github.com/kubernetes-sigs/kind/releases/download/v0.7.0/kind-$(uname)-amd64
~ $ chmod +x ./kind
~ $ sudo mv ./kind /usr/local/bin/kind
~ $ kind --version
kind version 0.7.0

With that, we are ready to setup our cluster. For that we will need following YAML file:

kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
        authorization-mode: "AlwaysAllow"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
- role: worker
- role: worker

This manifest describes our cluster. It will have 3 nodes - control plane (role: control-plane) and 2 workers role: worker. We are also giving it a few more settings and arguments to make it possible to setup ingress controller later, so that we can have HTTPS on this cluster. All you need to know about those settings, is that extraPortMappings tells cluster to forward ports from the host to an ingress controller running on a node.

Note: All the manifests for both cluster and Python application are available in my repo here in k8s directory.

Now, we need to run few commands to bring it up:

$ ~ kind create cluster --config kind-config.yaml --name cluster
$ ~ kubectl cluster-info --context kind-cluster
Kubernetes master is running at https://127.0.0.1:32769
KubeDNS is running at https://127.0.0.1:32769/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

$ ~ kubectl get nodes
NAME                    STATUS    ROLES     AGE       VERSION
cluster-control-plane   Ready     master    2m39s     v1.17.0
cluster-worker          Ready     <none>    2m3s      v1.17.0
cluster-worker2         Ready     <none>    2m3s      v1.17.0

To create cluster, we just need to run the first command. After that we can check whether it's good to go by running cluster-info and get nodes commands. Typing out these commands gets annoying after some time, so we will Make it simpler later, but with that we have cluster up and running.

Next, we want to setup ingress for our cluster. For that we have to run a few kubectl commands to make it work with KinD:

~ $ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/mandatory.yaml
~ $ kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/static/provider/baremetal/service-nodeport.yaml
~ $ kubectl patch deployments -n ingress-nginx nginx-ingress-controller -p \
  '{"spec":{"template":{"spec":{"containers":[{"name":"nginx-ingress-controller","ports":[{"containerPort":80,"hostPort":80},{"containerPort":443,"hostPort":443}]}],"nodeSelector":{"ingress-ready":"true"},"tolerations":[{"key":"node-role.kubernetes.io/master","operator":"Equal","effect":"NoSchedule"}]}}}}'

First we deploy mandatory ingress-nginx components. On top of that we expose the nginx service using NodePort, which is what the second command does. Last command applies some KinD specific patches for ingress controller.
Defining Manifests

With cluster ready, it's time to setup and deploy our application. For that we will use very simple Flask application - echo server:

# __main__.py

from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def echo():
    return f"You said: {request.args.get('text', '')}\n"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

I chose Flask application instead of some CLI tool (or Python package), as we need the application that won't terminate instantaneously, as some Python package would. Also, notice host parameter being set to 0.0.0.0, without this it would not be possible to reach the application when we expose it through Kubernetes service and ingress.

Next thing we need is YAML manifests for this application, let's break it up into separate objects:

- Namespace:

apiVersion: v1
kind: Namespace
metadata:
  name: blueprint

Nothing to really talk about here. We generally don't want to deploy applications in default namespace, so this is the one will use instead.

- ConfigMap:

apiVersion: v1
kind: ConfigMap
metadata:
  name: env-config-blueprint
  namespace: blueprint
data:  # Example vars that will get picked up by Flask application
  FLASK_ENV: development
  FLASK_DEBUG: "1"

This is where we can define variables for the application. These vars from data section will be injected into application container as environment variables. As an example, I included FLASK_ENV and FLASK_DEBUG, which will be picked up by Flask automatically when the application starts.

- Secret:

apiVersion: v1
kind: Secret
metadata:
  name: env-secrets-blueprint
  namespace: blueprint
data:
  VAR: VkFMVUU=  # base64 of "VALUE"

The same way as we specified plaintext vars, we can use Secret to add things like credential and keys to our application. This object should however, not be pushed to your repository as it contains sensitive data. We can create it dynamically with following command:

~ $ kubectl create secret generic env-secrets-blueprint -n blueprint \
    --from-literal=VAR=VALUE \
    --from-literal=VAR2=VALUE2 \
    --dry-run -o yaml >> app.yaml

Note: This and other commands, needed to deploy the application are listed in README in repository as well as at the bottom manifests file here

- Deployment:

apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: blueprint
  name: blueprint
  namespace: blueprint
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: blueprint
    spec:
      containers:
#        - image: docker.pkg.github.com/martinheinz/python-project-blueprint/example:flask
#          ^^^^^  https://github.com/containerd/containerd/issues/3291 https://github.com/kubernetes-sigs/kind/issues/870
        - image: martinheinz/python-project-blueprint:flask
          name: blueprint
          imagePullPolicy: Always
          ports:
            - containerPort: 5000
              protocol: TCP
          envFrom:
            - configMapRef:
                name: env-config-blueprint
            - secretRef:
                name: env-secrets-blueprint
#      imagePullSecrets:  # In case you are using private registry (see kubectl command at the bottom on how to create regcred)
#        - name: regcred
  selector:
    matchLabels:
      app: blueprint

Now for the most important part - the Deployment. The relevant part here is the spec section which specifies image, ports and environment variables. For image we specify image from Docker Hub. In case we wanted to use some private registry like Artifactory, we would have to add imagePullSecret which gives the cluster credential for pulling the image. This secret can be created using following command:

kubectl create secret docker-registry regcred \
    --docker-server=docker.pkg.github.com \
    --docker-username=<USERNAME> --docker-password=<GITHUB_TOKEN> \
    --dry-run -o yaml >> app.yaml

This shows how you would allow pulling of your images from GitHub Package Registry, which unfortunately doesn't work with KinD right now, because of issues listed in the above YAML, but it would work just fine with your production cluster in Cloud (assuming it's not using KinD).

If you want to avoid pushing image to remote registry every time you redeploy your application, then you can load your image into cluster using kind load docker-image martinheinz/python-project-blueprint:flask.

After image, we also specify ports. These are ports on which our application is listening on, in this case 5000, because our app starts using app.run(host='0.0.0.0', port=5000).

Last part, the envFrom section is used to inject plaintext variables and secrets from ConfigMap and Secret shown above, by specifying their names in the respective Ref fields.

- Service:

apiVersion: v1
kind: Service
metadata:
  name: blueprint
  namespace: blueprint
  labels:
    app: blueprint
spec:
  selector:
    app: blueprint
  ports:
    - name: http
      targetPort: 5000  # port the container accepts traffic on
      port: 443  # port other pods use to access the Service
      protocol: TCP

Now, that we have application listening on a port, we need Service that will expose it. All this objects defines is that application listening on port 5000 should be exposed on cluster node on port 443.

- Ingress:

apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: blueprint-ingress
  namespace: blueprint
  annotations:
    nginx.ingress.kubernetes.io/ssl-passthrough: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
  labels:
    app: blueprint
spec:
  tls:
    - hosts:
      - localhost
      secretName: tls-secret
  rules:
    - host: localhost
      http:
        paths:
          - path: "/"
            backend:
              serviceName: blueprint
              servicePort: 443

Last big piece of puzzle - the Ingress - an object that manages external access to the Services in a cluster. Let's first look at the rules section - in this case we define that our host is localhost. We also set path to / meaning that any request sent to localhost/ belongs to associated backend defined by name of the previously shown Service and its port.

The other section here is tls. This section provides HTTPS for listed hosts by specifying Secret that includes tls.crt and tls.key. Let's create this Secret:

KEY_FILE="blueprint.key"
CERT_FILE="blueprint.crt"
HOST="localhost"
CERT_NAME=tls-secret
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ${KEY_FILE} -out ${CERT_FILE} -subj "/CN=${HOST}/O=${HOST}"
kubectl create secret tls ${CERT_NAME} --key ${KEY_FILE} --cert ${CERT_FILE} --dry-run -o yaml >> app.yaml

Above snippet first sets a few variables which are then used to generate certificate and key files for TLS using openssl. Last command creates Secret containing these 2 files.
Deploying Application

With all the manifests ready, we can finally deploy our application:

$ ~ kubectl config set-context kind-cluster --namespace blueprint

$ ~ KEY_FILE="blueprint.key"
$ ~ CERT_FILE="blueprint.crt"
$ ~ HOST="localhost"
$ ~ CERT_NAME=tls-secret

$ ~ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ${KEY_FILE} -out ${CERT_FILE} -subj "/CN=${HOST}/O=${HOST}"

$ ~ kubectl create secret generic env-secrets-blueprint --from-literal=VAR=VALUE --dry-run -o yaml >> app.yaml && echo "---" >> app.yaml
$ ~ kubectl create secret tls ${CERT_NAME} --key ${KEY_FILE} --cert ${CERT_FILE} --dry-run -o yaml >> app.yaml

$ ~ kubectl apply -f app.yaml
namespace/blueprint unchanged
deployment.apps/blueprint created
configmap/env-config-blueprint unchanged
service/blueprint created
ingress.extensions/blueprint-ingress unchanged
secret/env-secrets-blueprint configured
secret/tls-secret configured

$ ~ kubectl get all
NAME                             READY   STATUS    RESTARTS   AGE
pod/blueprint-5d86484b76-dkw7z   1/1     Running   0          13s

NAME                TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/blueprint   ClusterIP   10.96.253.31   <none>        443/TCP   13s

NAME                        READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/blueprint   1/1     1            1           13s

NAME                                   DESIRED   CURRENT   READY   AGE
replicaset.apps/blueprint-5d86484b76   1         1         1       13s

$ ~ curl -k https://localhost/?text=Hello
You said: Hello

Most of the commands above we've already seen in sections before. What's new is kubectl apply -f app.yaml which creates all the necessary object in our cluster. After it's created we can check presence of those objects using kubectl get all. Finally we can check whether the application is accessible using cURL and it is! So, with that, we have our application running on the cluster!
Make-ing It Simple

If you don't feel fully comfortable with all the kind and kubectl commands yet or you are just lazy like me and you don't want to type it all out, then I have couple of Make targets for you - to make your life easier:

- Bring up the cluster:

cluster:
 @if [ $$(kind get clusters | wc -l) = 0 ]; then \
  kind create cluster --config ./k8s/cluster/kind-config.yaml --name kind; \
 fi
 @kubectl cluster-info --context kind-kind
 @kubectl get nodes
 @kubectl config set-context kind-kind --namespace $(MODULE)

The make cluster command will setup the cluster for you if it's not yet ready and if it is, it will give you all the info about it. This is nice if you need to check status of nodes and switch to your development namespace.

- Redeploy/Restart application:

deploy-local:
 @kubectl rollout restart deployment $(MODULE)

This one is very simple - all it does is roll out new deployment - so in case there is new image, it will deploy it, otherwise it will just restart your application.

- Debugging:

cluster-debug:
 @echo "\n${BLUE}Current Pods${NC}\n"
 @kubectl describe pods
 @echo "\n${BLUE}Recent Logs${NC}\n"
 @kubectl logs --since=1h -lapp=$(MODULE)

In case you need to debug your application, you will probably want to see recent events related to the application pod as well as recent (last hour) logs. That's exactly what make cluster-debug does for you.

- Get remote shell:

cluster-rsh:
 # if your container has bash available
 @kubectl exec -it $$(kubectl get pod -l app=${MODULE} -o jsonpath="{.items[0].metadata.name}") -- /bin/bash

If logs are not enough to solve some issues you might be having and you decide that you need to poke around inside the container, then you can run make cluster-rsh to get remote shell.

- Update manifests:

manifest-update:
 @kubectl apply -f ./k8s/app.yaml

We've seen this command before. It just re-applies YAML manifests, which is handy when you are tweaking some properties of Kubernetes objects.
Conclusion


https://medium.com/avmconsulting-blog/running-a-python-application-on-kubernetes-aws-56609e7cd88c

docker build -t dataprocess .
docker run -dp 3000:3000 dataprocess


docker tag cbe5e63196ba

 docker run --add-host jssqltaos:192.168.0.168 --add-host  jssqlredis:192.168.0.168 --add-host  jssqlmosquitto:192.168.0.168  --add-host  jssqlmysql:192.168.0.168  -ti dataprocess


 docker commit mysql2
 docker tag mysql:5.7 caijie73/mysql2:latest
 docker images
 https://opensource.com/article/18/1/running-python-application-kubernetes
 
 docker tag cbe5e63196ba caijie73/python3.6



This article wasn't meant to be Kubernetes tutorial, but I think it shows enough to get you started and have your application up and running pretty quickly. To learn more about Kubernetes, I recommend just playing, tweaking and changing things around in manifests and seeing what happens. That's in my opinion good way to find out how things work and to get comfortable with kubectl commands. If you have any questions, suggestions or issues feel free to reach out to me or create issue in my repository. In this repo, you can also find docs and all the manifests shown in this post. 
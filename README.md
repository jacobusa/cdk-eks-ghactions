[![ci](https://github.com/jacobusa/cdk-eks-ghactions/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/jacobusa/cdk-eks-ghactions/actions/workflows/ci.yml)

# One Click Deploy Microservices

Fully automated one click deploy of a microservice using cdk and github actions pipeline. Features many state of the art devops tools to deploy a python flask app with postgresql database into an eks cluster on AWS. Included is a local development environment using docker-compose, cdk setup with VPC, EKS, SSL cert management, Route53, and fully automated pipeline using github actions.

<br>

> **_MANUAL STEP_:** The only bootstrapping that is not automated is the manual change of nameservers from your domain registrar to the cdk created hosted zone in route53. Once you run the pipeline once, change the nameservers in your registrar to the route53 name servers and then wait until the app is running at app.DOMAIN.com, grafana.DOMAIN.com, and prometheus.DOMAIN.com. Once the nameservers are configured, you may need to delete the cluster certificates (1 in default namespace and 2 in monitoring namespace) and then run the pipeline again for the certificates to take effect.

<br>

> **_GITHUB ACTIONS:_** Before you run the github actions pipeline, be sure to enter the variables in the .env.example file into github actions secrets.
> <br>

<img width="990" alt="image" src="https://github.com/jacobusa/cdk-eks-ghactions/assets/49039999/d317c110-2a88-4ee0-a272-9985c6693070">
<img width="1439" alt="image" src="https://github.com/jacobusa/cdk-eks-ghactions/assets/49039999/dbc719b2-6e76-4126-b7ea-d1d763a4203a">
<img width="1440" alt="image" src="https://github.com/jacobusa/cdk-eks-ghactions/assets/49039999/52ecac21-d009-47f1-86c4-129ffe106b33">



## Tools

- Python Flask weather API with migrations equiped
- PostgreSQL database
- Docker and docker-compose for container management
- AWS CDK (VPC, EKS, Route53)
- NGINX Ingress Controller Network Load Balancer
- Prometheus Monitoring scraping metrics from flask app, postgres, and nginx load balancer
- Grafana dashboard
- Route53 domain configuration for prometheus (prometheus.<DOMAIN>.com, grafana.<DOMAIN>.com, app.<DOMAIN>.com)
- SSL Cert management using cert-manager and letsencrypt for domains above
- Github actions pipeline steps
  - Build and test application
  - Build docker image and push with cache
  - Deploy CDK network and cluster stack changes
  - Configuration of EKS Cluster
  - Deploy cdk route stack with resources built in EKS cluster

## To run the flask app locally,

```bash
source source .venv/bin/activate
mv .env.example .env
# fill out the .env file
pip install -r requirements.txt
docker-compose up
make run-migraions
make run-dev
```

## To deploy cdk stack manually

```bash
source source .venv/bin/activate
mv .env.example .env
# fill out the .env file
pip install -r requirements-cdk.txt
cdk deploy network-stack
cdk deploy cluster-stack
# Must have the nginx load balancer already deployed in the kubernetes cluster and it's dns name available as env NLB_DOMAIN
# To obtain the dns name of the nginx load balancer, run
# kubectl get svc ingress-nginx-controller -n ingress-nginx -o=jsonpath='{.status.loadBalancer.ingress[0].hostname}'
# Also must pass in the domain you want to deploy to hosted zone
export DOMAIN=<DOMAIN>
cdk deploy route-stack --parameters route-stack:nlbDomain=$NLB_DOMAIN --parameters route-stack:appDomain=$DOMAIN
```

## Global Teardown

- Manually delete the created nginx network load balancer from aws console.

```bash
cdk destroy --all
```

## Grafana dashboard

Once the application is successfully deployed, you can access the grafana dashboard available at grafana.YOUR-DOMAIN. A number of helpful dashboards can be added to visualize the data.

- Postgres dashboard, id: `9628`
- Flask dashboard, see `dashboards` folder for json to import to view flask app.
- NGINX dashboard, id: `9614`

## To access pgadmin

- For local development, after `docker-compose up` has been run, go to localhost:8888 in browser. The connection host to create is host.docker.internal and the secret is in the docker-compose file.

### More about CDK

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project. The initialization process also creates
a virtualenv within this project, stored under the .venv directory. To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ make test
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

- `cdk ls` list all stacks in the app
- `cdk synth` emits the synthesized CloudFormation template
- `cdk deploy` deploy this stack to your default AWS account/region
- `cdk diff` compare deployed stack with current state
- `cdk docs` open CDK documentation

Enjoy!

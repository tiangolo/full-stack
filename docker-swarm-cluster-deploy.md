# Cluster setup with Docker Swarm Mode and Traefik

This guide shows you how to create a cluster of Linux servers managed with Docker Swarm mode to deploy your projects.

It also shows how to set up an integrated main Traefik load balancer / proxy to receive incoming connections, re-transmit communication to Docker containers based on the domains, generate TLS / SSL certificates (for HTTPS) with Let's Encrypt and handle HTTPS.

## Install a new Linux server with Docker

* Create a new remote server (VPS).
* If you can create a `swap` disk partition, do it based on the [Ubuntu FAQ for swap partitions](https://help.ubuntu.com/community/SwapFaq#How_much_swap_do_I_need.3F).
* Deploy the latest Ubuntu LTS version image.
* Connect to it via SSH, e.g.:

```bash
ssh root@172.173.174.175
```

* Define a server name using a subdomain of a domain you own, for example `dog.example.com`.
* Create a temporal environment variable with the name of the host to be used later, e.g.:

```bash
export USE_HOSTNAME=dog.example.com
```

* Set up the server `hostname`:

```bash
# Set up the server hostname
echo $USE_HOSTNAME > /etc/hostname
hostname -F /etc/hostname
```

* Update packages:

```bash
# Install the latest updates
apt-get update
apt-get upgrade -y
```

* Install Docker:

```bash
# Download Docker
curl -fsSL get.docker.com -o get-docker.sh
# Install Docker
sh get-docker.sh
# Remove Docker install script
rm get-docker.sh
```

* Optionally, install [Netdata](http://my-netdata.io/) for server monitoring:

```bash
# Install Netdata
bash <(curl -Ss https://my-netdata.io/kickstart.sh)
```

* Generate and print SSH keys:

```bash
# Generate SSH keys
ssh-keygen -f $HOME/.ssh/id_rsa -t rsa -N ''
# Print SSH public key
cat ~/.ssh/id_rsa.pub
```

* Copy the key printed on screen. Something like:

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDdhjLuVOqpK+4+Fn7Nb0zrLJlbnAWqTjInB1vldFJX2J0Vmyss90qth7k/nhrAWX98cDey+dxcX35DYHRe9tsniaADKcnyYGUVY9yitswhZjeGVM/p8qdu6Qin2Oc+ZK9D8HGs3jDVxDG58UzoQGgiRvNsFZ2hhykK9oknO2gAiDcZiPW/UgbJyrlKdIps6ZO2qrCpajSyJDGVf7hDg7HepGv6YA8e4Tpf5iEXdHsm/9wRIL+dAHK4Kau53+D5yGo9Tmp3/H86DBaFrzA4x/Q556aOe/EvBbxEZdtaCXT5JVjhxLYr8eeg9xrg5ic9W2xj2xfdTT8jucLoPnh434+9 user@examplelaptop
```

* You can use that public key to import it in your Git server (GitLab, GitHub, Bitbucket) as a deployment server. That way, you will be able to pull your code to that server easily.


## Set up swarm mode

In Docker Swarm Mode you have one or more "manager" nodes and one or more "worker" nodes (that can be the same manager nodes).

The first step, is to configure one (or more) manager nodes.

* On the main manager node, run:

```bash
docker swarm init
```

* On the main manager node, for each additional manager node you want to set up, run:

```bash
docker swarm join-token manager
```

* Copy the result and paste it in the additional manager node's terminal, it will be something like:

```bash
 docker swarm join --token SWMTKN-1-5tl7yaasdfd9qt9j0easdfnml4lqbosbasf14p13-f3hem9ckmkhasdf3idrzk5gz 172.173.174.175:2377
```

* On the main manager node, for each additional worker node you want to set up, run:

```bash
docker swarm join-token worker
```

* Copy the result and paste it in the additional worker node's terminal, it will be something like:

```bash
docker swarm join --token SWMTKN-1-5tl7ya98erd9qtasdfml4lqbosbhfqv3asdf4p13-dzw6ugasdfk0arn0 172.173.174.175:2377
```

## Traefik

Set up a main load balancer with Traefik that handles the public connections and Let's encrypt HTTPS certificates.

* Create a network that will be shared with Traefik and the containers that should be accessible from the outside, with:

```bash
docker network create --driver=overlay traefik-public
```

* Create an environment variable with your email, to be used for the generation of Let's Encrypt certificates:

```bash
export EMAIL=admin@example.com
```

* Create a Traefik service:

```bash
docker service create \
    --name traefik \
    --constraint=node.role==manager \
    --publish 80:80 \
    --publish 8080:8080 \
    --publish 443:443 \
    --mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock \
    --mount type=volume,source=traefik-public-certificates,target=/certificates \
    --network traefik-public \
    traefik \
    --docker \
    --docker.swarmmode \
    --docker.watch \
    --docker.exposedbydefault=false \
    --constraints=tag==traefik-public \
    --entrypoints='Name:http Address::80' \
    --entrypoints='Name:https Address::443 TLS' \
    --acme \
    --acme.email=$EMAIL \
    --acme.storage=/certificates/acme.json \
    --acme.entryPoint=https \
    --acme.onhostrule=true \
    --acme.acmelogging=true \
    --logLevel=DEBUG \
    --web
```

The previous command explained:

* `docker service create`: create a Docker Swarm mode service
* `--name traefik`: name the service "traefik"
* `--constraint=node.role==manager` make it run on a Swarm Manager node
* `--publish 80:80`: listen on ports 80 - HTTP
* `--publish 8080:8080`: listen on port 8080 - HTTP for Traefik web UI
* `--publish 443:443`: listen on port 443 - HTTPS
* `--mount type=bind,source=/var/run/docker.sock,target=/var/run/docker.sock`: communicate with Docker, to read labels, etc.
* `--mount type=volume,source=traefik-public-certificates,target=/certificates`: create a volume to store TLS certificates
* `--network traefik-public`: listen to the specific network traefik-public
* `traefik`: use the image traefik:latest
* `--docker`: enable Docker
* `--docker.swarmmode`: enable Docker Swarm Mode
* `--docker.watch`: enable "watch", so it reloads its config based on new stacks and labels
* `--docker.exposedbydefault=false`: don't expose all the services, only services with traefik.enable=true
* `--constraints=tag==traefik-public`: only show services with traefik.tag=traefik-public, to isolate from possible intra-stack traefik instances
* `--entrypoints='Name:http Address::80'`: create an entrypoint http, on port 80
* `--entrypoints='Name:https Address::443 TLS'`: create an entrypoint https, on port 443 with TLS enabled
* `--acme`: enable Let's encrypt
* `--acme.email=$EMAIL`: let's encrypt email, using the environment variable
* `--acme.storage=/certificates/acme.json`: where to store the Let's encrypt TLS certificates - in the mapped volume
* `--acme.entryPoint=https`: the entrypoint for Let's encrypt - created above
* `--acme.onhostrule=true`: get new certificates automatically with host rules: "traefik.frontend.rule=Host:web.example.com"
* `--acme.acmelogging=true`: log Let's encrypt activity - to debug when and if it gets certificates
* `--logLevel=DEBUG`: log everything, to debug configurations and config reloads
* `--web`: enable the web UI, at port 8080

To check if it worked, check the logs:

```bash
docker service logs traefik
# To make it scrollable with `less`, run:
# docker service logs traefik | less
```


## Portainer

Create a Portainer web UI integrated with Traefik that allows you to use a web UI to see the state of your Docker services with:

```bash
docker service create \
    --name portainer \
    --label "traefik.frontend.rule=Host:portainer.$USE_HOSTNAME" \
    --label "traefik.enable=true" \
    --label "traefik.port=9000" \
    --label "traefik.tags=traefik-public" \
    --label "traefik.docker.network=traefik-public" \
    --label "traefik.frontend.entryPoints=http,https" \
    --constraint 'node.role==manager' \
    --network traefik-public \
    --mount type=bind,src=//var/run/docker.sock,dst=/var/run/docker.sock \
    portainer/portainer \
    -H unix:///var/run/docker.sock
```


## GitLab Runner

If you use GitLab and want to integrate Continuous Integration / Continuous Deployment, you can follow this section.

To install a GitLab runner in Docker Swarm mode run:

```bash
docker service create \
    --name gitlab-runner \
    --constraint 'node.role==manager' \
    --mount type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
    --mount src=gitlab-runner-config,dst=/etc/gitlab-runner \
    gitlab/gitlab-runner:latest
```

After that, check in which node the service is running with:

```bash
docker service ps gitlab-runner
```

You will get an output like:

```
root@dog:~/code# docker service ps gitlab-runner
ID                  NAME                IMAGE                         NODE                DESIRED STATE       CURRENT STATE            ERROR               PORTS
eybbh93ll0iw        gitlab-runner.1     gitlab/gitlab-runner:latest   cat.example.com     Running             Running 33 seconds ago
```

Then SSH to the node running it (in the example above it would be `cat.example.com`), e.g.:

```bash
ssh root@cat.example.com
```

In that node, run a `docker exec` command to register it, use auto-completion ( with `tab` ) for it to fill the name of the container, e.g.:

```bash
docker exec -it gitlab-ru
```

...and then hit `tab`.

Complete the command with the [GitLab Runner registration setup](https://docs.gitlab.com/runner/register/index.html#docker), e.g.:

```bash
docker exec -it gitlab-runner.1.eybbh93lasdfvvnasdfh7 bash
```

* Go to the GitLab "Admin Area -> Runners" section.
* Get the URL and create a variable in your Docker Manager's Terminal, e.g.:

```bash
export GITLAB_URL=https://gitlab.example.com/
```

* Get the registration token and create a variable in your Docker Manager's Terminal, e.g.:

```bash
export GITLAB_TOKEN=WYasdfJp4sdfasdf1234
```

* Run the next command editing the name and tags as you need.

```bash
gitlab-runner \
    register -n \
    --name "Docker Runner" \
    --tag-list dog-cat-cluster,stag,prod \
    --executor docker \
    --docker-image docker:latest \
    --docker-volumes /var/run/docker.sock:/var/run/docker.sock \
    --url $GITLAB_URL \
    --registration-token $GITLAB_TOKEN
```

* You can edit the runner more from the GitLab admin section.


## Deploy a stack

* Check a Docker Compose file like `docker-compose.prod.yml` with your stack.
* The services that should be exposed to the public network should have the `traefik-public` network besides the `default` network.
* Deploy the stack with, e.g.:

```bash
docker stack deploy -c docker-compose.yml name-of-my-stack
```
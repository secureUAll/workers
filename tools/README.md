# How to add a tool to the local docker registry

1. List all docker images:

```bash
    sudo docker image ls
```

2. Copy "IMAGE ID" from your tool.

3. Tag your image:

```bash
    sudo docker tag [image_ID] localhost/[image_name]:v1
```

4. Push your image to the docker registry:

```bash
sudo docker push localhost/[image_name]:v1
```

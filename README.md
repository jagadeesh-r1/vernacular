# vernacular
## Task given for Software Developer Role

Hi Devs,

The updated Docker image size is 132MB

## The Steps to follow in order to Build and Start the Docker Container

# To install docker-compose

1. Run this command to download the current stable release of Docker Compose:
    ```
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```
2. Apply executable permissions to the binary:
    ```
    sudo chmod +x /usr/local/bin/docker-compose
    ```

# To build the container

```
docker-compose build
```

# To run the container

```
docker-compose up
```

## API endpoints present

    ```
    http://127.0.0.1:8000/validate_finite_values  # task_1 api
    http://127.0.0.1:8000/validate_numeric_values # task_2 api
    ```
### The Postman API collection is the docs folder.
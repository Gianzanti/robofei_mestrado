# To start dev environment

- create a dir
- uv init --lib

> if desired, set the local config user for git:
>
> ```bash
> git config user.name "Name"
> git config user.email "Email"
> ```

- mount the Dockerfile

- mount the docker-compose.yml

- create the run.sh

- give it the run privilege:

```bash
chmod +x ./run.sh
```

- run it

After it is running, open vscode and install extensions Docker and Dev Container

Click on the left-bottom icon and attach vscode to the running container

After attached, install the needed extensions on container


(https://www.youtube.com/watch?v=6OxqiEeCvMI)

Dev Containers on vscode
https://www.youtube.com/watch?v=p9L7YFqHGk4

UV on Containers
https://www.youtube.com/watch?v=mFyE9xgeKcA


### To start running the tests:
```bash
uv run pytest -s
```

### To start running the tests and capture video:
```bash
MUJOCO_GL=egl uv run pytest -s
```



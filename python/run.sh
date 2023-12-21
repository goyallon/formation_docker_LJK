xhost +local:root
docker run -ti -v /home/goyallot/code/:/home/ -v $PWD:/data -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix formation_docker

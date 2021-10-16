#!/bin/bash
# This script run your submission inside a docker image, this is identical in termrs of
# how your code will be executed on AIcrowd platform, with the exception of some
# environment variables removed (which do not work outside AICrowd platform)

if [ -e environ_secret.sh ]
then
    echo "Note: Gathering environment variables from environ_secret.sh"
    source utility/environ_secret.sh
else
    echo "Note: Gathering environment variables from environ.sh"
    source utility/environ.sh
fi

# Skip building docker image on run, by default each run means new docker image build
if [[ " $@ " =~ " --no-build " ]]; then
    echo "Skipping docker image build"
else
    echo "Building docker image, for skipping docker image build use \"--no-build\""
    ./utility/docker_build.sh
fi

# Source secrets
if [ -e utility/secrets.sh ]
then
    source utility/secrets.sh
fi

# Expected Env variables : in environ.sh
if [[ " $@ " =~ " --nvidia " ]]; then
    nvidia-docker run \
    --net=host \
    --ipc=host \
    --user 0 \
    -v $(pwd):/home/aicrowd/code \
    -v /scr-ssd/divgarg/datasets/minerl:/home/aicrowd/data \
    -v $(pwd)/performance:/home/aicrowd/performance \
    -v $(pwd)/.gradle:/home/aicrowd/.gradle \
    -it ${IMAGE_NAME}:${IMAGE_TAG} \
    /bin/bash
else
    echo "To run your submission with nvidia drivers, use \"--nvidia\" with this script"
    docker run \
    --net=host \
    --user 0 \
    -it ${IMAGE_NAME}:${IMAGE_TAG} \
    /bin/bash
fi

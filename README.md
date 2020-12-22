# Applications

## Instructions
These instructions have been tested on a clean Ubuntu 20.04 installation running on a CloudLab C6420 machine.
Make sure you have sudo access and at least 100GB free space for application datasets and logs.

Clone the repository and submodules
```
git clone --recurse-submodules https://github.com/project-kona/apps.git
```

Set up applications and download data sets
(this will take a long time and it is best to launch this inside a screen session)
```
cd apps/scripts
./setup.sh
```

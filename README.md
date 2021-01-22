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
cd apps/script
./setup.sh
```

## Additional setup instructions for pintools runs

These instructions have been tested on a clean Ubuntu 16.04.1 LTS installation on a CloudLab c220g2 machine (profile: [ubuntu16-bare](https://www.cloudlab.us/show-profile.php?uuid=a18d69ba-06c7-11e8-a52e-90e2ba22fee4)).

After executing all the commands in the [Instructions](./README.md#Instructions) Section above, run also the following command (from the project root folder):

```
cd apps/script
./setup.sh pintool
```

<div class="warning">

**NOTE:**
1. These instructions and the pintools are not supported on Ubuntu 20.04.
2. You might get the following error during the installation of pip packages: `ERROR: pip's legacy dependency resolver does not consider dependency conflicts when selecting packages.` Just ignore this.

</div>
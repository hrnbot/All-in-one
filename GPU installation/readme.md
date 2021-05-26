# Install GPU and CUDA Driver in AWS GRID drivers (G3 and G4dn instances)

## Install GRID
```shell
$ sudo apt-get update -y
$ sudo apt-get upgrade -y linux-aws
$ sudo reboot
$ sudo apt-get install -y gcc make linux-headers-$(uname -r)
```
### Disable ```nouveau```
```shell
$ cat << EOF | sudo tee --append /etc/modprobe.d/blacklist.conf
blacklist vga16fb
blacklist nouveau
blacklist rivafb
blacklist nvidiafb
blacklist rivatv
EOF
```

### Edit the ```/etc/default/grub``` file and add the following line
```shell
$ GRUB_CMDLINE_LINUX="rdblacklist=nouveau"
$ sudo update-grub
```

### Add Access key
```shell
$ aws configure
```
```
Output:
AWS Access Key ID []:
AWS Secret Access Key []:
Default region name [us-east-2]:
Default output format [json]:
```

### Install GRID
```shell
$ aws s3 cp --recursive s3://ec2-linux-nvidia-drivers/latest/ .
$ chmod +x NVIDIA-Linux-x86_64*.run
$ sudo /bin/sh ./NVIDIA-Linux-x86_64*.run
$ sudo reboot
```
|  Note: Install other CUDA Driver ```aws s3 ls --recursive s3://ec2-linux-nvidia-drivers/```|
| --- |

## CUDA Install
```shell
$ wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
$ sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
$ sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/7fa2af80.pub
$ sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
$ sudo apt-get update
$ sudo apt-get -y install cuda
```


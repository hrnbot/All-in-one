# Anaconda Installation

|  Note: Follow for GUI QT ```apt-get install libgl1-mesa-glx libegl1-mesa libxrandr2 libxrandr2 libxss1 libxcursor1 libxcomposite1 libasound2 libxi6 libxtst6``` |
| --- |

## Download and Install Anaconda
```shell
$ wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
$ bash ~/Anaconda3-2021.05-Linux-x86_64.sh
$ source ~/.bashrc
```

## Anaconda sh-1
```shell
#!/bin/bash
conda activate env_name
```

### Execution 
```bash -i file_name.sh```

## Anaconda sh-2
```shell
eval $(conda shell.bash hook)
source /home/param/anaconda3/bin/activate env_name
echo "end"
```

### Execution 
```source file_name.sh```




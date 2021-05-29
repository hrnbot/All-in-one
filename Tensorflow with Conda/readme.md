# Install Pytorch with and without GPU

[GPU Guide Link](https://www.tensorflow.org/install/source#linux)

## Tensorflow  with GPU

### Tensorflow 2.5  python 3.6-3.9

```shell
$ pip install tensorflow==2.5
$ conda install cudatoolkit=11.2 cudnn=8.1
```

### Tensorflow 2.4 python 3.6-3.8

```shell
$ pip install tensorflow==2.4
$ conda install cudatoolkit=11.0 cudnn=8.0
```

### Tensorflow 2.1-2.3 python 3.5-3.8 (except 2.1 have 3.7)

```shell
$ pip install tensorflow==2.1-2.3
$ conda install cudatoolkit=10.1 cudnn=7.6.5
```

### Tensorflow 2.0 python 3.3-3.7

```shell
$ pip install tensorflow==2.0
$ conda install cudatoolkit=10.0 cudnn=7.4
```

### Tensorflow 1.13.1-1.15 python 3.3-3.7

```shell
$ conda install tensorflow_gpu=1.13.1-1.15
```

### Tensorflow 1.0.0-1.12 python  3.3-3.6

```shell
$ conda install tensorflow_gpu=1.0.0-1.12
```

## Tensorflow on CPU

|NOTE: It is beneficial to use tensorflow CPU when not using GPU because it is optimized for multi core CPU as well as reduces the installation size. |
|---|

### Tensorflow 2.5  python 3.6-3.9

```shell
$ pip install tensorflow==2.5
```

### Tensorflow 2.4 python 3.6-3.8

```shell
$ pip install tensorflow==2.4
```

### Tensorflow 2.1-2.3 python 3.5-3.8 (except 2.1 have 3.7)

```shell
$ pip install tensorflow==2.1-2.3
```

### Tensorflow 2.0 python 3.3-3.7

```shell
$ pip install tensorflow==2.0
```

### Tensorflow 1.13.1-1.15 python 3.3-3.7

```shell
$ conda install tensorflow=1.13.1-1.15
```

### Tensorflow 1.0.0-1.12 python  3.3-3.6

```shell
$ conda install tensorflow=1.0.0-1.12
```



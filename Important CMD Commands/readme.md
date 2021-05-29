### Installation of Package
If you know the name of the package, then you can easily install a program using this command:

```shell
sudo apt-get install <package-name> 
```

### Remove Package

- When it comes to removing the installed program apt-get remove command suits your need. You only have to know the exact
package name of the software you want to uninstall.
  ```shell
  sudo apt-get remove <package-name>
  ```
  |NOTE:If you don’t know the package name, use below ubuntu basic command to list all the packages installed on your system and then copy the package name from the list: ```dpkg --list```|
  |---| 

- apt-get purge command is used when you want to remove a software completely from your system with its configuration or
data files so that no longer personalized settings will be available during reinstallation.
  ```shell
  sudo apt-get purge <package-name>
  ```
  
- apt-get autoremove command is used to remove any unnecessary packages. Unnecessary means, whenever you install an
  application, the system will also install the software that this application depends on. It is common in Ubuntu that
  applications share the same libraries. When you remove the application the dependency will stay on your system.
  ```shell
  sudo apt-get autoremove
  ```
  
### System Info 
- du (directory usage) command displays the size of a directory and all of its subdirectories.
  ```shell
  du
  ```
  
- df (display filesystem) command displays information about the disk space usage of all mounted filesystems.
  ```shell
  df -h 
  ```
  
- free – Displays the amount of free space available on the system.
  ```shell
  free 
  ```
  
- uname -a – Provides a wide range of basic information about the system.
  ```shell
  uname -a
  ```
  
- top – Displays the processes using the most system resources at any given time. “q” can be used to exit.
  ```shell
  top
  ```

### Manage Processes
- The command “ps” which is also known as process status command is used to provide information about the processes
  currently running on the system, including their respective process identification numbers (PIDs).
  ```shell
  ps
  ps -ef #every running process (-e) and a full listing (-f).
  ps -ef |grep process_name #short name will also work to show filtered name
  pgrep process_name #Alternative of "ps -ef |grep process_name"
  ```
  
- A process may not continue to run when you log out or close your terminal. This special case can be avoided by
  preceding the command you want to run with the nohup command. Also, appending an ampersand (&) will send the process
  to the background and allow you to continue using the terminal.
  ```shell
  nohup myprogram.sh &
  ```
  
- The top command has been around a long time and is very useful for viewing details of running processes and quickly
  identifying issues such as memory hogs. Its default view is shown below.
  ```shell
  top -p2020 #2020 is PID value
  ```
  
- Interestingly, there is no stop command. In Linux, there is the kill command. Kill is used to send a signal to a
  process. The most commonly used signal is "terminate" (SIGTERM) or "kill" (SIGKILL).
  ```shell
  kill -9 20896 #To kill a process
  ```
  
### Other 
- The command “head” prints the top N rows of data of the given input or file. By default, it prints the first 10 lines
  of the specified files.
  ```shell
  head -n File_name
  ```
  
- The command “tail” prints the last N rows of data of the given input or file. By default, it prints the last 10 lines
  of the specified files.
  ```shell
  tail -n File_name
  ```
  
- The command “zip” is used to compress one or more files and store them in a new file with .zip extension.
  ```shell
  zip Files.zip Check.txt Test.txt Output.txt
  ```
  
- The command “unzip” is used to decompress a .zip file and extract all the files within to current directory.
  ```shell
  unzip Files.zip
  ```
  
- The command “whereis” is self-explanatory, as it displays the path where the package for specific built-in Linux
  command locates.
  ```shell
  whereis python3.8
  ```
- This will empty whole cache files. A lot of space could be freed if you frequently install and uninstall softwares.
  ```shell
  sudo apt-get clean
  ```
  
- It will remove old dependent files and footprints installed by previous applications.
  ```shell
  sudo apt-get automove
  ```

  

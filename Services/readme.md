# Service File Writing
A unit configuration file whose name ends in ".service" encodes information about a process controlled and supervised by
systemd.

## Create a New Service
```shell
$ sudo nano /etc/systemd/system/service_name.service
```
```shell
[Unit]
Description= Description of service
After=network.target
[Service]
User=ubuntu
Group=www-data
Restart=always
WorkingDirectory=/home/ubuntu/repo_dir
Environment="PATH=/home/ubuntu/anaconda3/envs/env_name"
ExecStart=/home/ubuntu/anaconda3/envs/env_name/bin/python manage.py runserver 0.0.0.0:8000 #If run without gunicorn
#ExecStart=/home/ubuntu/anaconda3/envs/env_name/bin/gunicorn --bind 0.0.0.0:8000 myproject.wsgi #If run with gunicorn
[Install]
WantedBy=multi-user.target
```

# Detail Explanation

## [Unit] Section Directives

The first section found in most unit files is the [Unit] section. This is generally used for defining metadata for the
unit and configuring the relationship of the unit to other units.

Although section order does not matter to systemd when parsing the file, this section is often placed at the top because
it provides an overview of the unit. Some common directives that you will find in the [Unit] section are:

- **Description**= This directive can be used to describe the name and basic functionality of the unit. It is returned by
  various systemd tools, so it is good to set this to something short, specific, and informative.
  

- **Documentation**= This directive provides a location for a list of URIs for documentation. These can be either
  internally available man pages or web accessible URLs. The systemctl status command will expose this information,
  allowing for easy discoverability.
  

- **Requires**=: This directive lists any units upon which this unit essentially depends. If the current unit is activated,
  the units listed here must successfully activate as well, else this unit will fail. These units are started in
  parallel with the current unit by default.
  

- **Wants**=: This directive is similar to Requires=, but less strict. Systemd will attempt to start any units listed here
  when this unit is activated. If these units are not found or fail to start, the current unit will continue to
  function. This is the recommended way to configure most dependency relationships. Again, this implies a parallel
  activation unless modified by other directives.
  

- **BindsTo**=: This directive is similar to Requires=, but also causes the current unit to stop when the associated unit
  terminates.
  

- **Before**=: The units listed in this directive will not be started until the current unit is marked as started if they
  are activated at the same time. This does not imply a dependency relationship and must be used in conjunction with one
  of the above directives if this is desired.
  

- **After**=: The units listed in this directive will be started before starting the current unit. This does not imply a
  dependency relationship and one must be established through the above directives if this is required.
  

- **Conflicts**=: This can be used to list units that cannot be run at the same time as the current unit. Starting a unit
  with this relationship will cause the other units to be stopped.
  

- **Condition...**=: There are a number of directives that start with Condition which allow the administrator to test
  certain conditions prior to starting the unit. This can be used to provide a generic unit file that will only be run
  when on appropriate systems. If the condition is not met, the unit is gracefully skipped.
  

- **Assert...**=: Similar to the directives that start with Condition, these directives check for different aspects of the
  running environment to decide whether the unit should activate. However, unlike the Condition directives, a negative
  result causes a failure with this directive
  

## [Install] Section Directives

On the opposite side of unit file, the last section is often the [Install] section. This section is optional and is used
to define the behavior or a unit if it is enabled or disabled. Enabling a unit marks it to be automatically started at
boot. In essence, this is accomplished by latching the unit in question onto another unit that is somewhere in the line
of units to be started at boot.

- **WantedBy**=: The WantedBy= directive is the most common way to specify how a unit should be enabled. This directive
  allows you to specify a dependency relationship in a similar way to the Wants= directive does in the [Unit] section.
  The difference is that this directive is included in the ancillary unit allowing the primary unit listed to remain
  relatively clean. When a unit with this directive is enabled, a directory will be created within /etc/systemd/system
  named after the specified unit with .wants appended to the end. Within this, a symbolic link to the current unit will
  be created, creating the dependency. For instance, if the current unit has WantedBy=multi-user.target, a directory
  called multi-user.target.wants will be created within /etc/systemd/system (if not already available) and a symbolic
  link to the current unit will be placed within. Disabling this unit removes the link and removes the dependency
  relationship.
  

- **RequiredBy**=: This directive is very similar to the WantedBy= directive, but instead specifies a required dependency
  that will cause the activation to fail if not met. When enabled, a unit with this directive will create a directory
  ending with .requires.
  

- **Alias**=: This directive allows the unit to be enabled under another name as well. Among other uses, this allows
  multiple providers of a function to be available, so that related units can look for any provider of the common
  aliased name.
  
  
- **Also**=: This directive allows units to be enabled or disabled as a set. Supporting units that should always be
  available when this unit is active can be listed here. They will be managed as a group for installation tasks.
  

- **DefaultInstance**=: For template units (covered later) which can produce unit instances with unpredictable names, this
  can be used as a fallback value for the name if an appropriate name is not provided.
  
## The [Service] Section

The [Service] section is used to provide configuration that is only applicable for services.

One of the basic things that should be specified within the [Service] section is the Type= of the service. This
categorizes services by their process and daemonizing behavior. This is important because it tells systemd how to
correctly manage the servie and find out its state.

- **simple**: The main process of the service is specified in the start line. This is the default if the Type= and Busname=
  directives are not set, but the ExecStart= is set. Any communication should be handled outside of the unit through a
  second unit of the appropriate type (like through a .socket unit if this unit must communicate using sockets).
  

- **forking**: This service type is used when the service forks a child process, exiting the parent process almost
immediately. This tells systemd that the process is still running even though the parent exited.


- **oneshot**: This type indicates that the process will be short-lived and that systemd should wait for the process to exit
  before continuing on with other units. This is the default Type= and ExecStart= are not set. It is used for one-off
  tasks.
  

- **dbus**: This indicates that unit will take a name on the D-Bus bus. When this happens, systemd will continue to process
  the next unit.
  

- **notify**: This indicates that the service will issue a notification when it has finished starting up. The systemd
  process will wait for this to happen before proceeding to other units.
  

- **idle**: This indicates that the service will not be run until all jobs are dispatched.

So far, we have discussed some pre-requisite information, but we haven’t actually defined how to manage our services. The directives to do this are:

- **ExecStart**=: This specifies the full path and the arguments of the command to be executed to start the process. This
  may only be specified once (except for “oneshot” services). If the path to the command is preceded by a dash “-”
  character, non-zero exit statuses will be accepted without marking the unit activation as failed.
  

- **ExecStartPre**=: This can be used to provide additional commands that should be executed before the main process is
  started. This can be used multiple times. Again, commands must specify a full path and they can be preceded by “-” to
  indicate that the failure of the command will be tolerated.
  

- **ExecStartPost**=: This has the same exact qualities as ExecStartPre= except that it specifies commands that will be run
  after the main process is started.
  

- **ExecReload**=: This optional directive indicates the command necessary to reload the configuration of the service if
  available.
  

- **ExecStop**=: This indicates the command needed to stop the service. If this is not given, the process will be killed
  immediately when the service is stopped.
  

- **ExecStopPost**=: This can be used to specify commands to execute following the stop command.


- **RestartSec**=: If automatically restarting the service is enabled, this specifies the amount of time to wait before
  attempting to restart the service.
  

- **Restart**=: This indicates the circumstances under which systemd will attempt to automatically restart the service. This
  can be set to values like “always”, “on-success”, “on-failure”, “on-abnormal”, “on-abort”, or “on-watchdog”. These
  will trigger a restart according to the way that the service was stopped.
  

- **TimeoutSec**=: This configures the amount of time that systemd will wait when stopping or stopping the service before
  marking it as failed or forcefully killing it. You can set separate timeouts with TimeoutStartSec= and TimeoutStopSec=
  as well.
  

## The [Socket] Section

Socket units are very common in systemd configurations because many services implement socket-based activation to
provide better parallelization and flexibility. Each socket unit must have a matching service unit that will be
activated when the socket receives activity.

By breaking socket control outside of the service itself, sockets can be initialized early and the associated services
can often be started in parallel. By default, the socket name will attempt to start the service of the same name upon
receiving a connection. When the service is initialized, the socket will be passed to it, allowing it to begin
processing any buffered requests.

- **ListenStream**=: This defines an address for a stream socket which supports sequential, reliable communication. Services
  that use TCP should use this socket type.
  

- **ListenDatagram**=: This defines an address for a datagram socket which supports fast, unreliable communication packets.
  Services that use UDP should set this socket type.
  

- **ListenSequentialPacket**=: This defines an address for sequential, reliable communication with max length datagrams that
  preserves message boundaries. This is found most often for Unix sockets.
  

- **ListenFIFO**: Along with the other listening types, you can also specify a FIFO buffer instead of a socket.


- **Accept**=: This determines whether an additional instance of the service will be started for each connection. If set to
  false (the default), one instance will handle all connections.
  

- **SocketUser**=: With a Unix socket, specifies the owner of the socket. This will be the root user if left unset.


- **SocketGroup**=: With a Unix socket, specifies the group owner of the socket. This will be the root group if neither this
  or the above are set. If only the SocketUser= is set, systemd will try to find a matching group.
  

- **SocketMode**=: For Unix sockets or FIFO buffers, this sets the permissions on the created entity.


- **Service**=: If the service name does not match the .socket name, the service can be specified with this directive.


## The [Mount] Section

Mount units allow for mount point management from within systemd. Mount points are named after the directory that they
control, with a translation algorithm applied.

For example, the leading slash is removed, all other slashes are translated into dashes “-”, and all dashes and
unprintable characters are replaced with C-style escape codes. The result of this translation is used as the mount unit
name. Mount units will have an implicit dependency on other mounts above it in the hierarchy.

Mount units are often translated directly from /etc/fstab files during the boot process. For the unit definitions
automatically created and those that you wish to define in a unit file, the following directives are useful:


- **What**=: The absolute path to the resource that needs to be mounted.


- **Where**=: The absolute path of the mount point where the resource should be mounted. This should be the same as the unit
  file name, except using conventional filesystem notation.
  

- **Type**=: The filesystem type of the mount.


- **Options**=: Any mount options that need to be applied. This is a comma-separated list.


- **SloppyOptions**=: A boolean that determines whether the mount will fail if there is an unrecognized mount option.


- **DirectoryMode**=: If parent directories need to be created for the mount point, this determines the permission mode of
  these directories.
  

- **TimeoutSec**=: Configures the amount of time the system will wait until the mount operation is marked as failed.


## The [Automount] Section

This unit allows an associated .mount unit to be automatically mounted at boot. As with the .mount unit, these units
must be named after the translated mount point’s path.

The [Automount] section is pretty simple, with only the following two options allowed:


- **Where**=: The absolute path of the automount point on the filesystem. This will match the filename except that it uses
  conventional path notation instead of the translation.
  

- **DirectoryMode**=: If the automount point or any parent directories need to be created, this will determine the
  permissions settings of those path components.
  

## The [Swap] Section

Swap units are used to configure swap space on the system. The units must be named after the swap file or the swap
device, using the same filesystem translation that was discussed above.

Like the mount options, the swap units can be automatically created from /etc/fstab entries, or can be configured
through a dedicated unit file.

The [Swap] section of a unit file can contain the following directives for configuration:

- **What**=: The absolute path to the location of the swap space, whether this is a file or a device.


- **Priority**=: This takes an integer that indicates the priority of the swap being configured.


- **Options**=: Any options that are typically set in the /etc/fstab file can be set with this directive instead. A
  comma-separated list is used.
  

- **TimeoutSec**=: The amount of time that systemd waits for the swap to be activated before marking the operation as a
failure.


## The [Path] Section

A path unit defines a filesystem path that systmed can monitor for changes. Another unit must exist that will be be
activated when certain activity is detected at the path location. Path activity is determined thorugh inotify events.

The [Path] section of a unit file can contain the following directives:

- **PathExists**=: This directive is used to check whether the path in question exists. If it does, the associated unit is
  activated.
  

- **PathExistsGlob**=: This is the same as the above, but supports file glob expressions for determining path existence.


- **PathChanged**=: This watches the path location for changes. The associated unit is activated if a change is detected
  when the watched file is closed.
  

- **PathModified**=: This watches for changes like the above directive, but it activates on file writes as well as when the
  file is closed.
  

- **DirectoryNotEmpty**=: This directive allows systemd to activate the associated unit when the directory is no longer
  empty.
  

- **Unit**=: This specifies the unit to activate when the path conditions specified above are met. If this is omitted,
  systemd will look for a .service file that shares the same base unit name as this unit.
  

- **Unit**=: This specifies the unit to activate when the path conditions specified above are met. If this is omitted,
  systemd will look for a .service file that shares the same base unit name as this unit.
  

- **MakeDirectory**=: This determines if systemd will create the directory structure of the path in question prior to
  watching.
  

- **DirectoryMode**=: If the above is enabled, this will set the permission mode of any path components that must be
  created.
  

## The [Timer] Section

Timer units are used to schedule tasks to operate at a specific time or after a certain delay. This unit type replaces
or supplements some of the functionality of the cron and at daemons. An associated unit must be provided which will be
activated when the timer is reached.

The [Timer] section of a unit file can contain some of the following directives:


- **OnActiveSec**=: This directive allows the associated unit to be activated relative to the .timer unit’s activation.


- **OnBootSec**=: This directive is used to specify the amount of time after the system is booted when the associated unit
  should be activated.
  

- **OnStartupSec**=: This directive is similar to the above timer, but in relation to when the systemd process itself was
  started.
  

- **OnUnitActiveSec**=: This sets a timer according to when the associated unit was last activated.


- **OnUnitInactiveSec**=: This sets the timer in relation to when the associated unit was last marked as inactive.


- **OnCalendar**=: This allows you to activate the associated unit by specifying an absolute instead of relative to an
  event.
  

- **AccuracySec**=: This unit is used to set the level of accuracy with which the timer should be adhered to. By default,
  the associated unit will be activated within one minute of the timer being reached. The value of this directive will
  determine the upper bounds on the window in which systemd schedules the activation to occur.
  

- **Unit**=: This directive is used to specify the unit that should be activated when the timer elapses. If unset, systemd
  will look for a .service unit with a name that matches this unit.
  

- **Persistent**=: If this is set, systemd will trigger the associated unit when the timer becomes active if it would have
  been triggered during the period in which the timer was inactive.
  

- **WakeSystem**=: Setting this directive allows you to wake a system from suspend if the timer is reached when in that
  state.
  




  


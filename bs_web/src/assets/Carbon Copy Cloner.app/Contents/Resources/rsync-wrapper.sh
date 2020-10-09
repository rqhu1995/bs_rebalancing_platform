#!/bin/sh

PATH=/bin:/usr/bin:/sbin:/usr/sbin export PATH

# rsync-wrapper shell script.  Copyright 2002-2014, Mike Bombich
# This script is executed when the root user from a remote machine
# successfully authenticates with a public key.  The privileges
# of that user on this server are limited to the functionality of this script.
# This wrapper will verify that the client is sending an rsync command.
# If it is, then the original, unaltered command is run, if not, 
# an error is returned.

log="/Library/Application Support/com.bombich.ccc/pht_debug.log"
mkdir -p "/Library/Application Support/com.bombich.ccc"
require_codesign=FALSE
read_only=FALSE

# Lion is 11, ML is 12, Mavericks is 13, Yosemite is 14
os=`/usr/sbin/sysctl -n kern.osrelease | awk -F. '{print $1}'`

if [ "${SSH_ORIGINAL_COMMAND:=UNSET}" == "UNSET" ]; then
        echo "root login is not permitted to this machine via public key authentication." | tee -a "$log"
        exit 127
fi

declare -a command
command=($SSH_ORIGINAL_COMMAND)

# Is this an rsync request?
echo "${command[*]}" | /usr/bin/grep -e "^/private/var/root/rsync" >> /dev/null
rsyncRequest=$?

# Is this an scp request?
echo "${command[*]}" | /usr/bin/grep -e "^scp -t " | /usr/bin/grep -e " /private/var/root/rsync" -e " /private/var/root/archive_manager" >> /dev/null
scpRequest=$?

# Is this an archive_manager request?
echo "${command[*]}" | /usr/bin/grep -e "^/private/var/root/archive_manager" >> /dev/null
amRequest=$?

CAFFEINATE=""
if [ -x /usr/bin/caffeinate ]; then
	# -m (prevent disk sleep) was added in Mavericks
	if [ $os -lt 13 ]; then
		CAFFEINATE="/usr/bin/caffeinate -is"
	else
		CAFFEINATE="/usr/bin/caffeinate -ims"
	fi
fi


# Make sure the original command is rsync
if [ "$rsyncRequest" == "0" ]; then
	if [ "$require_codesign" == "TRUE" ]; then
		/usr/bin/codesign -v -R='certificate root = H"611E5B662C593A08FF58D14AE22452D198DF6C60" and certificate leaf[subject.O] = "Bombich Software"* and identifier "rsync"' /private/var/root/rsync
		if [ ! $? = 0 ]; then
			exit 13
		fi
	fi

	# Ensure that --server is on the command line, to enforce running
	# rsync in server mode. If required, verify that --sender is specified

	server=false
	sender=false
	for arg in "${command[@]}"; do
		if [ "$arg" == "--sender" ]; then
			sender=true
		fi
		if [ "$arg" == "--server" ]; then
			server=true
		fi
	done
	
	if [ "$read_only" == "TRUE" -a "$sender" == "false" ]; then
		echo "This server requires read-only requests" | tee -a "$log"
		exit 125
	fi

	# If the command is an rsync server, execute the original command
	if [ "$server" == "true" ]; then
		$CAFFEINATE $SSH_ORIGINAL_COMMAND
	else
		echo "This does not appear to be a valid rsync request" | tee -a "$log"
		exit 125
	fi

elif [ "$scpRequest" == "0" ]; then
	now=`date '+%m/%d %H:%M:%S'`
	printf "$now\tRemoving older binaries\n" >> "$log"
	/usr/bin/find /private/var/root \( -name "rsync.*" -or -name "archive_manager.*" \) -mtime +3d -exec rm '{}' \; 2>> /dev/null
	# Also remove any existing copy of the executable that is getting copied here. We do this because scp doesn't
	# do atomic copies, and the kernel will return cached codesigning results if it thinks an executable file hasn't changed
	old_exec=`echo "${command[*]}" | awk '{print $NF}'`
	if [ -f "$old_exec" ]; then
		echo "Removing $old_exec" >> "$log"
		rm "$old_exec"
	fi
	$SSH_ORIGINAL_COMMAND

elif [ "$amRequest" == "0" ]; then
	now=`date '+%m/%d %H:%M:%S'`
	echo "$now\tCalling archive_manager: $SSH_ORIGINAL_COMMAND" >> "$log"
	$CAFFEINATE $SSH_ORIGINAL_COMMAND

elif [ "${command[0]}" == "enableOwnership" ]; then
	now=`date '+%m/%d %H:%M:%S'`
	tgt=`echo "$SSH_ORIGINAL_COMMAND" | cut -c 17-`
	printf "$now\tEnabling ownership on $tgt\n" >> "$log"
	/usr/sbin/diskutil enableOwnership "$tgt" | tee -a "$log"
	exit 0

elif [ "${command[0]}" == "update_dyld_shared_cache" ]; then
	tgt=`echo "$SSH_ORIGINAL_COMMAND" | cut -c 26-`
	if [ -f "$tgt/System/Library/CoreServices/SystemVersion.plist" -a -x "$tgt"/usr/bin/update_dyld_shared_cache ]; then
		now=`date '+%m/%d %H:%M:%S'`
		printf "$now\tUpdating the macOS \"Dynamic Linker Shared Cache\" on \"$tgt\"\n" >> "$log"
		$CAFFEINATE "$tgt"/usr/bin/update_dyld_shared_cache -root "$tgt" >> "$log" 2>> "$log" &
	fi
	exit 0

elif [ "${command[0]}" == "unlockCSEVolume" ]; then
	now=`date '+%m/%d %H:%M:%S'`
	tgt=`echo "$SSH_ORIGINAL_COMMAND" | cut -c 17-`
	printf "$now\tMounting $tgt\n" >> "$log"
	/usr/sbin/diskutil cs info "$tgt" >> "$log"
	devID=`/usr/sbin/diskutil cs info "$tgt" | awk '/Device Identifier/ {print $NF}'`
	if [ "$devID" = "" ]; then
		devID=`/usr/sbin/diskutil cs unlockVolume "$tgt" -stdinpassphrase | awk '/Core Storage disk:/ {print $NF}' | tee -a "$log"`
	fi

	if [ "$devID" != "" ]; then
		printf "$now\tMounting device attached at $devID\n" >> "$log"
		printf "Diskutil mount result: `/usr/sbin/diskutil mount $devID`\n" | tee -a "$log"
	fi
	exit 0

elif [ "${command[0]}" == "unlockAPFSVolume" ]; then
	now=`date '+%m/%d %H:%M:%S'`
	volUUID=`echo "$SSH_ORIGINAL_COMMAND" | awk '{print $2}'`
	printf "$now\tMounting APFS with volume UUID $volUUID\n" >> "$log"
	/usr/sbin/diskutil info "$volUUID" >> "$log"
	/usr/sbin/diskutil ap unlock "$volUUID" -stdinpassphrase >> "$log"

	if [ "$devID" != "" ]; then
		printf "$now\tMounting device attached at $devID\n" >> "$log"
		printf "Diskutil mount result: `/usr/sbin/diskutil mount $devID`\n" | tee -a "$log"
	fi
	exit 0

elif [ "${command[0]}" == "mountVolume" ]; then
	now=`date '+%m/%d %H:%M:%S'`
	tgt=`echo "$SSH_ORIGINAL_COMMAND" | cut -c 13-`
	printf "$now\tAttempting to mount $tgt\n" >> "$log"
	/usr/sbin/diskutil mount "$tgt" | tee -a "$log"
	exit 0

elif [ "${command[0]}" == "unmountVolume" ]; then
	now=`date '+%m/%d %H:%M:%S'`
	tgt=`echo "$SSH_ORIGINAL_COMMAND" | cut -c 15-`
	printf "$now\tUnmounting $tgt\n" >> "$log"
	/usr/sbin/diskutil unmount "$tgt" | tee -a "$log"
	exit 0

elif [ "${command[0]}" == "ejectVolume" ]; then
	now=`date '+%m/%d %H:%M:%S'`
	tgt=`echo "$SSH_ORIGINAL_COMMAND" | cut -c 13-`
	printf "$now\tEjecting $tgt\n" >> "$log"
	/usr/sbin/diskutil eject "$tgt" | tee -a "$log"
	exit 0

else
	echo "Command rejected by rsync_wrapper: ${command[@]}" | tee -a "$log"
	echo "That command is not allowed with the root account via public key authentication."
	exit 125
fi

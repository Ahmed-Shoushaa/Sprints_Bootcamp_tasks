#!/bin/bash

is_root ()
{
 if [[ $EUID == 0 ]]; then
  echo "The User Have Root Privileges" 
  echo "================================================="
else
  echo "The User -$USER- Doesn't Have Root Privileges"
  echo "This script has commands that needs root privilege "
  echo "PLEASE SIGN IN AS A ROOT AND TRY AGAIN"
  echo "=========================================================="
  exit
 fi
}

ssh_port ()
{
 echo "CHANGING SSH PORT"
 echo "Please Enter The New SSH PORT"  
 echo "Note:The Port Number Must Be 22 or Between 1024 & 65535"
 echo "......................................................."
 read -p "New SSH Port->>" sshport
 sed -i -e "/Port /c\Port $sshport" /etc/ssh/sshd_config
 echo "changing SSH Port in 5 please wait"
 firewall-cmd --permanent --zone=public --add-port=$sshport/tcp
 firewall-cmd --reload
 semanage port -a -t ssh_port_t -p tcp $sshport
 systemctl restart sshd.service
 echo "The SSH Port has been changed successfuly to $sshport"
 echo "====================================================="
}

disable_root_login ()
{
 echo "Root Login Disable/Enable"
 echo "........................."   
 echo "Do you want to disable Root Login?[y,n]"
 read answer
 if [ "$answer" = "y" ]; then	 
  echo "Disbling Root Login in 5 please wait"
  sed -i -e "/PermitRootLogin /c\PermitRootLogin no" /etc/ssh/sshd_config
  firewall-cmd --reload
  systemctl restart sshd.service
  echo "Root login Is Disabled"
  echo "======================"
 else
  sed -i -e "/PermitRootLogi/c\#PermitRootLogin yes" /etc/ssh/sshd_config
  firewall-cmd --reload
  systemctl restart sshd.service
  echo "Root login still enabled"
  echo "================================"
 fi 
}

new_user ()
{
 echo "ADDING NEW USER"
 echo "..............." 
 read -p "Enter New User Name:" user
 adduser $user
 passwd $user
 echo "$user was Added successfully"
 echo "Do you want to add -- $user -- to the sudoers?[y,n}"
 read ans
 if [ "$ans" = y ]; then
  usermod -aG wheel $user
  echo "$user added to sudoers successfully"
  echo "==================================="
 else
  echo "$user isn't in the sudoers"
  echo "=========================="
 fi
}

home_backup ()
{
 read -p "Enter the user you want to backup his home dir->" usr
 echo "SCHEDULING USER HOME DIR. BACKUP"
 echo "................................"
 echo "Choose Crontab time if not write -- * --"
 echo "Minute  Hour  Day.In.Month  Month  Day.In.Week"
 read -p "Month (must be between 1-12):" month
 read -p "day in month (must be between 1-31):" dayInmonth
 read -p "hour (must be between 0-23):" hour
 read -p "minute (must be between 0-59):" min
 read -p "day in week (must be between 0-6) 0=sunday:" week_day
 #command="rsync -av /home/$usr /home/$usr/backup "
 command="tar -zcvpf /home/$usr/tar_backup /home/$usr/"
 job="$min $hour $dayInmonth $month $week_day $command"
 (crontab -l ; echo "$job") | crontab -
 #cat <(fgrep -i -v "$command" <(crontab -l)) <(echo "$job") | crontab -
 echo "command:< $job > was added successfully to the crontab"
}

is_root
ssh_port
disable_root_login
new_user
home_backup

#!/bin/bash

##the script must run by root privileges
##the script takes three arguments
##the FIRST argument  $1--> SSH PORT  NUMBER
##the SECOND argument $2--> New user name
##the third argument  $3--> User Password
port_num=$1
user_name=$2
pass=$3

if [ $# != 3 ]; then
 echo 'The script requires only three arguments(SSH PORT - USER NAME -USER PASSWORD) please enter them '
 exit 0
fi

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
is_root
ssh_port ()
{
 echo "Changing ssh port number"
 sed -i -e "/Port /c\Port $port_num" /etc/ssh/sshd_config
 #firewall-cmd --permanent --zone=public --add-port=$port_num/tcp
 #firewall-cmd --reload
 #semanage port -a -t ssh_port_t -p tcp $port_num
 #systemctl restart sshd.service
 echo "SSH Port changed to $port_num"
 echo "========================"
}
ssh_port
disable_root ()
{
 echo "Disabling Root Login"
 sed -i -e "/PermitRootLogin /c\PermitRootLogin no" /etc/ssh/sshd_config
 echo "Root Login Is Disabled"
 echo "======================"
}
disable_root
update_firewall()
{
 echo "Updating firewall and selinux and SSH service"
 echo "............................................."
 firewall-cmd --permanent --zone=public --add-port=$port_num/tcp
 firewall-cmd --reload
 semanage port -a -t ssh_port_t -p tcp $port_num
 systemctl restart sshd.service
 echo "Done"
 echo "===="
}
update_firewall
new_group ()
{
 echo "Adding a group --Audit--"
 echo "........................"
 groupadd -g 20000 Audit
 echo "--Audit-- was added with id -20000-"
 echo "==================================="
}
new_group
new_user ()
{
 echo "Adding a new user"
 useradd $user_name 
 echo "$user_name:$pass" | chpasswd
 echo "A new user -- $user_name -- added successfully"
 echo "====================================" 
}
new_user
year_reports ()
{
 echo "Making Reports for the year in user $user_name home directory"
 mkdir /home/$user_name/Reports
 touch /home/$user_name/Reports/2021-{01..12}-{01..31}.xls
 echo "Directory created"
 chmod 770 /home/$user_name/Reports
 echo "User $user_name and his group can only access the Directory" 
 echo "=================================================="
}
year_reports
update ()
{
 echo "Updating and Upgrading the system"
 echo "................................."
 yes | yum update
 echo "============================"
}
update
epel ()
{
 echo "enabling EPEL repo"
 dnf search epel
 dnf install epel-release -y 
 dnf config-manager --set-enabled PowerTools || dnf install 'dnf-command(config-manager)' -y
 dnf config-manager --set-enabled PowerTools
 dnf update
 dnf --disablerepo="*" --enablerepo="epel" list available | wc -l
 #yum repolist
}
epel
fail2ban () 
{ 
 echo "Installing fail2ban"
 dnf update -y && dnf install epel-release -y
 dnf install fail2ban sendmail -y
 systemctl enable --now fail2ban
 systemctl enable --now sendmail
 echo "===================================================="
}
fail2ban
reports_backup ()
{
 echo "Backing Reports directory"
 command="tar -zcvpf /root/backups/reports-WEEKNUMBER-DAYNUMBEROFTHEWEEK.tar /home/$2/Reports"
 job="00 01 * * 1-5 $command"
 (crontab -l ; echo "$job") | crontab -
 echo "command:< $job > was added successfully to the crontab"
 echo "Reports successfully backedup"
 echo "============================="
}
reports_backup
user_manager ()
{
 echo "Adding a new user --Manager-- with id --30000--"
 useradd Manager -u 30000
 echo "success"
 echo "Manager addedd to users successfully"
 echo "===================================="
}
user_manager

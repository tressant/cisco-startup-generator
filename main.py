service = ['hostname', 'vlan', 'interface', 'passwords', 'ssh', 'banner', 'disable unused ports', 'port security',
           'trunk', 'no dns lookup', 'trunk', 'router on a stick']
# clears config.txt
open('config.txt', 'w').close()
# opens config.txt in append mode so it can write each line at the end of the file
# need to change to context manager
config = open("config.txt", "a")
# output of list_to_num that is the index of all selected services
selected_services = []
ports = []


def service_hostname():
    """
    sets the hostname
    """
    host = input("hostname ")
    config.write("\nhostname " + host)


def service_vlan():
    """
    sets vlans
    """
    vlan_list = []
    while True:
        vlan_to_config = input('which vlan to config? ')
        if vlan_to_config == 'q' or vlan_to_config == 'quit':
            break
        else:
            config.write('\nvlan ' + vlan_to_config)
            vlan_name = input("what name to give vlan? ")
            config.write('\nname ' + vlan_name + '\nexit')
            vlan_list.append(vlan_to_config)
            vlan_list.sort()
    for x in range(0, len(vlan_list)):
        interface = input('apply vlan ' + str(vlan_list[x]) + ' to Fa0/')
        config.write('\nint Fa0/' + str(interface) + '\nswitchport access vlan ' + vlan_list[x] + '\nexit\n')
        x += 1
        print('switchport trunk native vlan {vlan number}')


def service_interface():
    """
    sets interfaces
    """
    while True:
        interface_type = input("interface type: ").lower().strip()
        if interface_type == 'g' or interface_type == 'gig' or interface_type == 'gigabit':
            toConfig = int(input("How many interfaces to config?"))
            for intToConfig in range(-1, int(toConfig)):
                ipToAssign = input("IP address and subnet for g0/" + str(toConfig) + ' ')
                config.write("\nint g0/" + str(toConfig) + "\nip address " + str(ipToAssign) + "\nno shut\nexit\n")
                int(toConfig)
                toConfig -= 1
        elif interface_type == 'fa' or interface_type == 'fast ethernet':
            toConfig = int(input("How many interfaces to config?"))
            for intToConfig in range(-1, int(toConfig)):
                ipToAssign = input("IP address and subnet for fa0/" + str(toConfig) + ' ')
                config.write("\nint fa0/" + str(toConfig) + "\nip address " + str(ipToAssign) + "\nno shut\nexit\n")
                int(toConfig)
                toConfig -= 1
        elif interface_type == 'l' or interface_type == 'loopback':
            ipToAssign = input('IP address and subnet for loopback')
            config.write('\nint loopback\nip address ' + str(ipToAssign) + '\nno shut\nexit\n')
        elif interface_type == 'vlan':
            while True:
                vlan = input("which vlan to config? ")
                if vlan != 'quit' or vlan != 'q':
                    ip_address = input("ip to assign to vlan " + str(vlan) + ' ')
                    config.write('\nint vlan' + str(vlan) + '\nip addr ' + ip_address + '\nno shut')
                else:
                    break
        elif interface_type == 'q' or interface_type == 'quit':
            break
        print('pick gigabit, fast ethernet, loopback, or vlan')


def service_passwords():
    """
    sets passwords
    """
    execPass = input("Exec mode pass ")
    config.write('\nenable pass ' + execPass)
    execSec = input('Exec mode secret ')
    config.write('\nenable sec ' + execSec)
    lineconPass = input('linecon pass ')
    config.write('\nline con 0\npass ' + lineconPass + '\nlogin\nexit')
    config.write('\nservice pass')


def service_port_security():
    """
    does the commands to let cisco know i know what port security is but i don't
    """
    print('only does Fa')
    while True:
        open_port = input('which ports are active? ')
        if open_port == 'q' or open_port == 'quit':
            break
        config.write('\nint Fa0/' + str(open_port) + '\nswitchport mode access\nswitchport port-security')
        config.write('\nswitchport port-security max 2\nswitchport port-security mac-address sticky\nexit\n')


def service_router_on_a_stick():
    print('f')
    while True:
        interface = input('which interface to configure\n(g0/0.x syntax) ')
        if interface == 'q': break
        config.write('\ninterface ' + str(interface))
        encapsulation = input('which vlan? ')
        config.write('\nencapsulation dot1q ' + str(encapsulation))
        ip_address = input('ip address to configure: ')
        config.write('\nip address ' + str(ip_address))


def port_list():
    """
    generates a list of all ports on a cisco switch
    """
    for x in range(1, 25):
        toAppend = 'Fa0/' + str(x)
        ports.append(toAppend)
    for x in range(1, 3):
        toAppend = 'G0/' + str(x)
        ports.append(toAppend)


def turn_off_ports():
    """
    turns off all ports generated by port_list()
    """
    for x in range(len(ports)):
        config.write('\nint ' + ports[x] + '\nshutdown\nexit\n')


def turn_on_ports():
    """
    turns back on the ports that you need because all ports should be off
    """
    while True:
        print('gig ports have index of 25 and 26')
        to_turn_on = str(input('which port to turn back on? '))
        # print(to_turn_on)
        if to_turn_on == 'q' or to_turn_on == 'quit':
            break
        else:
            config.write('\nint ' + ports[int(to_turn_on) - 1] + '\nno shut\nexit\n')


def service_ssh():
    """
    sets ssh
    """
    domain = input('define a domain name ')
    config.write('\nip domain-name ' + domain)
    ssh_user = input('ssh username ')
    ssh_pass = input('ssh pass ')
    config.write('\nusername ' + str(ssh_user) + ' sec ' + str(ssh_pass))
    bits = str(input("how many bits to gen for rsa key? "))
    config.write('\ncry key gen rsa\n' + bits)
    config.write('\nip ssh v 2\nip ssh auth 2\nip ssh time 60\n')
    telnet = input('disable telnet [y/n] ')
    if telnet == 'y':
        config.write('\nline vty 0 4\nlogin local\ntransport input ssh')


def service_banner():
    """
    sets banner
    """
    ban = input('banner (do not include any *) ')
    config.write('\nban motd *' + ban + '*\n')


def service_trunk():
    while True:
        interface = input('interface to config ').upper()
        if interface != 'q' or interface != 'quit':
            vlan = input('which vlan to apply? ')
            config.write('\nint ' + str(interface) + '\nswitchport mode trunk\n')
            config.write('switchport trunk native vlan ' + str(vlan))
        break


def service_no_dns_lookup():
    config.write('\nno ip domain-lookup')


def list_to_num():
    """
    takes user input and sends the selected services to a list
    """
    while True:
        service_selection = input("What service do you need? ")
        if service_selection.lower().strip() in service:
            print("service supported")
            index = int(service.index(service_selection))
            # print(index)
            selected_services.append(index)
            selected_services.sort()
            # print(selected_services)
        elif service_selection == 'quit' or service_selection == 'q':
            break
        elif service_selection == '--help':
            print("select a service from the list: " + str(service))
        else:
            print("not supported")
            print("supported services are " + str(service))


def generate_config():
    """
    takes the user selected services and applies them to config.txt
    """
    print(selected_services)
    while True:
        if 0 in selected_services:
            service_hostname()
            selected_services.remove(0)
        elif 1 in selected_services:
            service_vlan()
            selected_services.remove(1)
        elif 2 in selected_services:
            service_interface()
            selected_services.remove(2)
        elif 3 in selected_services:
            service_passwords()
            selected_services.remove(3)
        elif 4 in selected_services:
            service_ssh()
            selected_services.remove(4)
        elif 5 in selected_services:
            service_banner()
            selected_services.remove(5)
        elif 6 in selected_services:
            port_list()
            turn_off_ports()
            turn_on_ports()
            selected_services.remove(6)
        elif 7 in selected_services:
            service_port_security()
            selected_services.remove(7)
        elif 8 in selected_services:
            service_trunk()
            selected_services.remove(8)
        elif 9 in selected_services:
            service_no_dns_lookup()
            selected_services.remove(9)
        elif 10 in selected_services:
            service_trunk()
            selected_services.remove(10)
        elif 11 in selected_services:
            service_router_on_a_stick()
            selected_services.remove(11)
        else:
            break


print("'quit' to quit")
list_to_num()
# print(selected_services)
generate_config()

config.close()

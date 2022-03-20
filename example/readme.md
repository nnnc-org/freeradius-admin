# Example FreeRADIUS Server

Here is a very basic FreeRADIUS server config that can be setup via docker-compose. This config has default user, `bob`, that can be used with radclient to authenticate. In the post-auth config, if the Calling-Station-ID is a known device, you will receive VLAN 5, otherwise you get VLAN 4.

**Before trying to run this, make sure you update the `rest` config with a valid server url.**

Below is a sample command to use the radclient command wit output.

```
docker:/$ docker exec -it freeradius bash

# Example output of valid device

root@000000000000:/# echo "User-Name=bob,User-Password=hello,Calling-Station-Id=ac:de:48:00:00:00" | radclient 127.0.0.1:1812 auth testing123 -x
Sent Access-Request Id 172 from 0.0.0.0:33643 to 127.0.0.1:1812 length 62
	User-Name = "bob"
	User-Password = "hello"
	Calling-Station-Id = "ac:de:48:00:00:00"
	Cleartext-Password = "hello"
Received Access-Accept Id 172 from 127.0.0.1:1812 to 127.0.0.1:33643 length 47
	Reply-Message = "Hello, bob"
	Tunnel-Type:0 = VLAN
	Tunnel-Medium-Type:0 = IEEE-802
	Tunnel-Private-Group-Id:0 = "4"

# Example output of invalid device

root@000000000000:/# echo "User-Name=bob,User-Password=hello,Calling-Station-Id=dc:de:48:00:00:00" | radclient 127.0.0.1:1812 auth testing123 -x
Sent Access-Request Id 127 from 0.0.0.0:39351 to 127.0.0.1:1812 length 62
	User-Name = "bob"
	User-Password = "hello"
	Calling-Station-Id = "dc:de:48:00:00:00"
	Cleartext-Password = "hello"
Received Access-Accept Id 127 from 127.0.0.1:1812 to 127.0.0.1:39351 length 47
	Reply-Message = "Hello, bob"
	Tunnel-Type:0 = VLAN
	Tunnel-Medium-Type:0 = IEEE-802
	Tunnel-Private-Group-Id:0 = "5"
```
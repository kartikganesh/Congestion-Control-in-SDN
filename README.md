# Congestion-Control-in-SDN
Steps for the connection setup:

1.Download or clone the two files and copy them to /pox

2.cd ../pox

3.Make the scripts executable:
 
 $ chmod u+x pController.py
 
 $ chmod u+x pTopology.py

4.Make sure no other terminal windows are open with mininet running in the background

5.$ sudo killall controller

6.Restart Mininet to make sure that everything is clean
 
 $ sudo mn -c

7.Start the controller: ./pox.py pController

8. Open another terminal and go to the same location as above and type

sudo ./pTopology.py

Now you will obersve the topolgy is setup.

9. To verify it woks we run the command at switch s1 s2 s4:

sh ovs-ofctl dump-flows s1

sh ovs-ofctl dump-flows s2

sh ovs-ofctl dump-flows s4

10. Perform iperf tests at h1 and h4 with udp and other posrt numbers to see how different traffic is diverted.

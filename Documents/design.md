# coversnake
## Gary. K and Amir. Z
### 3/27/2022


[Github Link](https://github.com/d0ntblink/covertsnake)


### Intial Ideas
- maybe build a GUI for practice
- I want a progress bar (tqdm)
- implement key exchange if possible
- use scapy to change the header and send/recieve packets
- try 5 diffrent files to steal. a video, a picture, a audio, one doc and a zip file
- make a debug mode

### Hiding the Packets
since i cant use the id, sequnce or acknowledge seq i will use the length part of the IP header to hide information in. the packets will be DNS Quaries to google.com. since the  low number Bytes wont deliver since the lenght will be lower than the actual packet size, i will be add a 0xff to each byte and then taking it off on the server side.

the first packet send from the client has the name of the file encode via base64.
every byte after that is saved by the server and added to a bytearray to build back the file.

a google.ca (instead of google.com) dns quary will tell the server that all the information has been sent and it can write the file

TLDR: first a DNS query is sent to the server that has the file name encoded via base64 in it. then there are google.com queries sent to the server that have the infromation hidden in their IP.lenght header. a final google.ca dns query tells the server that all the bytes have been transfered and it can create the file.

### Rest of the script
- scapy will handle the packet creation and reading.
- files are open and written as binary in python
- tqdm used to build a progress bar for client
- base64 library used to encode and decode strings
- bytearray is used to hold Bytes before they are modified.
- for each byte before sending on the client side, 0xff is added to them and 0xff is taken off on the server side



### Soruces
https://github.com/zaheercena/Covert-TCP-IP-Protocol/blob/master/covert_tcp.c

https://github.com/syn53/packetagent

https://journals.uic.edu/ojs/index.php/fm/article/view/528/449

https://www.geeksforgeeks.org/progress-bars-in-python/

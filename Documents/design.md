# Assignment 4 - CoverSnake by Garshasb Khodayari and Amir Zilabi
### 3/27/2022
[Github Link](https://github.com/d0ntblink/covertsnake)

Team members divided the workload of this project into the following:

- Garshasb Khodayari - Application and Testing
- Amir Zilabi - Documentation and Design

## Design

### Initial Ideas

- Possible implementation of GUI for practice
- Implement a progress bar
- Possible implementation of key exchange
- Use Scapy to change the header and send/receive packets
- Implementation of a debug mode
- Create and test the script with 5 files:

1. Video
2. Image
3. Audio
4. Document
5. Zip file

## Hiding the Packets

Since we cannot use the ID, sequence, or acknowledge sequence, we will use the length section of the IP header to hide the relative information. In addition, the packets will be DNS Queries to **Google.com**. Consequently, since the low number of bytes will not deliver due to the length being lower than the actual packet size, we will add **0xff** to each byte and remove on the server side.

The first packet will be sent from the client which has the name of the file in base64; additionally, every byte after that is saved by the server and added to a byte array to build back the file.

**Too Long, Didn't Read (TLDR)** First DNS query is sent to the server that has the file name encoded in base64. On the side, there are **google.com** queries sent to the server that have the information hidden in their **IP.length header**. To finalize, a final **google.ca** DNS query will communicate with the server that all the bytes have been transferred and the file will be created.

## Rest of the Script

- Scapy will handle the packet creation and reading.
- Files are open and written as binary in Python
- TDQM used to build a progress bar for the client
- Base64 library used to encode and decode strings
- Byte array is used to hold bytes before they are modified.
- For every byte that will be sent from the client side, **0xff** is added to them and taken on the server side.

##Soruces

https://github.com/zaheercena/Covert-TCP-IP-Protocol/blob/master/covert_tcp.c

https://github.com/syn53/packetagent

https://journals.uic.edu/ojs/index.php/fm/article/view/528/449

https://www.geeksforgeeks.org/progress-bars-in-python/

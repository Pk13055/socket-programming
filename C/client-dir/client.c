// Client side C/C++ program to demonstrate Socket programming
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

#define PORT 8080
#define true 1
#define false 0
typedef int bool;

#define PACKET_SIZE 1024

int main(int argc, char const *argv[])
{
  struct sockaddr_in address;
  int sock = 0, valread;
  struct sockaddr_in serv_addr;
  char *filename[] = {"file1.txt", "file2.txt"};
  char buffer[5 * PACKET_SIZE] = {NULL};
  
  if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
      printf("\n Socket creation error \n");
      return -1;
    }

  memset(&serv_addr, '0', sizeof(serv_addr)); // to make sure the struct is empty. Essentially sets sin_zero as 0
  // which is meant to be, and rest is defined below

  serv_addr.sin_family = AF_INET;
  serv_addr.sin_port = htons((argc >= 2)? atoi(argv[1]) : PORT);

  // Converts an IP address in numbers-and-dots notation into either a
  // struct in_addr or a struct in6_addr depending on whether you specify AF_INET or AF_INET6.
  if(inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr)<=0)
    {
      printf("\nInvalid address/ Address not supported \n");
      return -1;
    }

  if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)  // connect to the server address
    {
      printf("\nConnection Failed \n");
      return -1;
    } 

  int no_of_files = 1, i;

  for (i = 0; i < no_of_files; i++) {

    send(sock , filename[i] , strlen(filename[i]) , 0 );  // send the message.
    printf("File name sent\n");

    // open the sent file ready for receiving
    int fd = open(filename[i], O_CREAT | O_WRONLY | O_APPEND, 0644);

    // error handling for opening the file
    if ( fd < 0 ) {
      perror("File failed to open.");
      return 1;
    }


    int   current_received = 0;
    bool first_run = true;
    // start IO loop to gather the file packets
    while(1) {

      // test print
      printf("READING: ");
      // receive message back from server, into the buffer
      valread = read(sock , buffer, PACKET_SIZE);


      // test print
      printf(" %d bytes\n",valread);

      // test print
      if (valread < 0) {
        perror("Unable to receive contents.");
        return 1;
      }

      else if ( valread == 0 ) {
        printf((first_run)? "No" : "Complete");
        printf(" file received\n");
        break;
      }

      first_run = false;
      current_received += valread;

      write(fd, buffer, valread);
    }

    printf("Total bytes received: %d\n", current_received);
    close(fd);
  
  }

  send(sock , "0" , 1 , 0 );  // send the ending messgae
  return 0;
}

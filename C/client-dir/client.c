// Client side C/C++ program to demonstrate Socket programming
#include <stdio.h>
#include <sys/socket.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>

#define PORT 8080

#define PACKET_SIZE 1

int main(int argc, char const *argv[])
{
    struct sockaddr_in address;
    int sock = 0, valread;
    struct sockaddr_in serv_addr;
    char *filename = "file1.txt";
    char buffer[1024] = {0};
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Socket creation error \n");
        return -1;
    }

    memset(&serv_addr, '0', sizeof(serv_addr)); // to make sure the struct is empty. Essentially sets sin_zero as 0
                                                // which is meant to be, and rest is defined below

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);

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
    
    send(sock , filename , strlen(filename) , 0 );  // send the message.
    printf("File name sent\n");
    
    int fd = open(filename, O_CREAT | O_WRONLY, S_IRWXU);
    // error handling for opening the file
    if ( fd < 0 ) {
      perror("File failed to open.");
      return 1;
    }

    while(1) {
      valread = read( sock , buffer, 1);
      // receive message back from server, into the buffer

      if ( valread == 0 ) {
        break;
      }

      else if (valread < 0) {
        perror("Unable to receive contents.");
        return 1;
      }

      // test print
      printf("%s\n",buffer );

      write(fd, buffer, strlen(buffer));

      strcpy("", buffer);
    }
    
    close(fd);
    return 0;
}

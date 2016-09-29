#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <unistd.h>

typedef struct {
  struct sockaddr_un* address;
  int id;
} SocketConnection;

void* initSocketConnection(const char* socketName,const char* filename) 
{

  SocketConnection *con = malloc(sizeof(SocketConnection));
  con->address = malloc(sizeof(struct sockaddr_un));

  int len;
  if ( (con->id = socket(AF_UNIX,SOCK_STREAM,0)) == -1 ){
    perror("socket");
    exit(1);
  }
con->address->sun_family = AF_UNIX;
  strcpy(con->address->sun_path,socketName);
  len = strlen(con->address->sun_path) + sizeof(con->address->sun_family);
  if ( connect(con->id,(struct sockaddr *)con->address,len) == -1 ) {
    perror("connect");
    exit(1);
  }

  len = strlen(filename)+1;
  if ( send(con->id,filename,len,0) < 0 ) {
    perror("sending filename");
    exit(1);
  }

  char status[10];
  int n;

  if ((n = recv(con->id,(void *)status,sizeof(status),0)) <= 0) {
    if (n < 0) perror("recv");
    else printf("Server closed connection\n");
    exit(1);
  }

  if (strncmp(status,"ready",5) != 0) {
    printf("eddy brake server not ready");
    exit(1);
  }

  return (void*) con;
}

void closeSocketConnection(void* object)
{
  SocketConnection *con = (SocketConnection*) object;
  close(con->id);
  free(con->address);
  free(con);
}

void getEddyBrakeData(void* object,
  double v,double h,
  double* f_drag,double* f_lift,
  double* H_y_max,double* H_y_mean,
  double* q_max,double* q_mean)
{

  SocketConnection *con = (SocketConnection*) object;

  double input[2];
  input[0] = v;
  input[1] = h;
  double output[6];

  int n;

  if (send(con->id,input,sizeof(input),0) < 0){
    perror("getEddyBrakeData send");
    exit(1);
  }
  if((n=recv(con->id,(void*)output,sizeof(output),0))<=0){
    if(n<0) perror("getEddyBrakeData recv");
    else printf("getEddyBrakeData server closed connection");
    exit(1);
  }
  *f_drag = output[0];
  *f_lift = output[1];
  *H_y_max = output[2];
  *H_y_mean = output[3];
  *q_max = output[4];
  *q_mean = output[5];
  return;
}

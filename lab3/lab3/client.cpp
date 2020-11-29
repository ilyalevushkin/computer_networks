#include "headers/client.h"

string file = "index.html";

void send_request(int sockfd, string file)
{
    stringstream request;
    request << "GET /" 
    << file.c_str() 
    << " HTTP/1.1 \nHost: 127.0.0.1:" 
    << SERVER_PORT << "\nConnection: close\n";
    
    cout << "Client request:\n" << request.str() << endl;
    write(sockfd, request.str().c_str(), request.str().length());
}

void get_response(int sockfd)
{
    char buffer[MSG_LEN + 1];
    bzero(buffer, sizeof(buffer));
    cout << "Server response:" << endl;
    int read_bytes = sizeof(buffer) - 1;
    while (read_bytes == sizeof(buffer) - 1)
    {
        read_bytes = read(sockfd, buffer, sizeof(buffer) - 1);
        cout << buffer;
        bzero(buffer, sizeof(buffer));
        fflush(stdout);
    }
    cout << endl;
}

int main(int argc, char** argv)
{
	if (argc > 1)
	{
        if (argc == 2)
        {
            file = argv[1];
        }
    }

    int sockfd = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sockfd < 0)
    {
        cout << "Error socket()" << endl;
        return SOCKET_ERR;
    }

    struct sockaddr_in client;
    memset(&client, 0, sizeof(client));

    client.sin_family = AF_INET;
    client.sin_addr.s_addr = INADDR_ANY;
    client.sin_port = htons(CLIENT_PORT);

    int number = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &number, sizeof(int));

    int ret = bind(sockfd, (const struct sockaddr*)&client, 
        sizeof(client));
    
    if (ret < 0)
    {
        close(sockfd);
        cout << "Error bind()" << endl;
        return BIND_ERR;
    }

    struct sockaddr_in server;
    memset(&server, 0, sizeof(server));

    server.sin_family = AF_INET;
    server.sin_port = htons(SERVER_PORT);
    server.sin_addr.s_addr = inet_addr("127.0.0.1");

    if (connect(sockfd, (const struct sockaddr*)&server, sizeof(server)) != 0)
    {
        close(sockfd);
        cout << "Error connect()" << endl;
        return CONNECT_ERR;
    }

    send_request(sockfd, file);

    get_response(sockfd);

    close(sockfd);

    return 0;
}

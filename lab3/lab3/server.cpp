#include "headers/server.h"


int sigint_f = 0;
int sockfd = 0;

queue<struct client_t> q;
pthread_t pool[POOL_SIZE];
pthread_cond_t condition = PTHREAD_COND_INITIALIZER;
pthread_mutex_t content_mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
map<string, map<string, int>> statistics_map;


int init_socket(int &sockfd)
{
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0)
    {
        cout << "Error socket()" << endl;
        return SOCKET_ERR;
    }

    struct sockaddr_in server;
    memset(&server, 0, sizeof(server));

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(SERVER_PORT);

    int number = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &number, sizeof(int));

    int ret = bind(sockfd, (const struct sockaddr*)&server, sizeof(server));
    if (ret < 0)
    {
        close(sockfd);
        cout << "Error bind()" << endl;
        return BIND_ERR;
    }

    if (listen(sockfd, LISTEN_COUNT) != 0)
    {
        close(sockfd);
        cout << "Error listen()" << endl;
        return LISTEN_ERR;
    }

    signal(SIGINT, sigint_handler);
    
    return 0;
}


void push_new_client(struct sockaddr_in &client, int &client_sock)
{
    struct client_t new_client;
    new_client.ip_addr = string(inet_ntoa(client.sin_addr))
        + ":" + to_string(ntohs(client.sin_port));
    new_client.socket = client_sock;

    pthread_mutex_lock(&mutex);
    q.push(new_client);
    pthread_cond_signal(&condition);
    pthread_mutex_unlock(&mutex);
}

int main(void)
{
    int ret = init_socket(sockfd);

    if (ret < 0)
    {
        return ret;
    }


    for (int i = 0; i < POOL_SIZE; i++)
    {
        pthread_create(&pool[i], nullptr, thread_f, nullptr);
    }


    struct sockaddr_in client;
    unsigned int client_size = sizeof(client);
    memset(&client, 0, client_size);

    cout << "Server is running..." << endl;
    while (1)
    {
        int client_sock = accept(sockfd, (struct sockaddr*)&client, &client_size);
        if (client_sock < 0)
        {
            close(sockfd);
            cout << "Error accept()" << endl;
            return ACCEPT_ERR;
        }

        push_new_client(client, client_sock);
    }

    close(sockfd);

    return 0;
}

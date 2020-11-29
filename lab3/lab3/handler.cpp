#include "headers/handler.h"

void sigint_handler(int signal)
{
    sigint_f = 1;
    close(sockfd);
    cout << "Closed by signal " << signal << endl;
    save_statistics_in_txt_file();
}

void* thread_f(void* argv)
{
    while (1)
    {
        struct client_t* pclient = nullptr;

        pthread_mutex_lock(&mutex);
        if (q.empty())
        {
            pthread_cond_wait(&condition, &mutex);
            pclient = &q.front();
            q.pop();
        }
        else
        {
            pclient = &q.front();
            q.pop();
        }
        pthread_mutex_unlock(&mutex);

        if (pclient != nullptr)
        {
            handle_f(*pclient);
        }
    }
}

void handle_f(struct client_t client)
{
    char buffer[MSG_LEN + 1];
    bzero(buffer, sizeof(buffer));
    read(client.socket, buffer, sizeof(buffer));

    string request = buffer;
    auto response = get_response(client, request);

    write(client.socket, response.c_str(), response.length());
}

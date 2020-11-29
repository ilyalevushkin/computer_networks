#pragma once

#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <csignal>
#include <pthread.h>
#include <sys/ioctl.h>


#include <queue>
#include <string>
#include <cstring>
#include <iostream>
#include <fstream>
#include <chrono>
#include <ctime>
#include <sstream>
#include <map>
#include <tuple>

#include "const.h"
#include "handler.h"
#include "parser.h"
#include "statistics.h"

using namespace std;


#define LISTEN_COUNT 1000
#define POOL_SIZE 10

extern int sockfd;
extern int sigint_f;

struct client_t
{
    string ip_addr;
    int socket;
};

extern queue<struct client_t> q;

extern pthread_t pool[POOL_SIZE];
extern pthread_mutex_t content_mutex;
extern pthread_mutex_t mutex;
extern pthread_cond_t condition;

extern map<string, map<string, int>> statistics_map;




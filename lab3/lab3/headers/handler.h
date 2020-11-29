#pragma once

#include "server.h"

using namespace std;

void sigint_handler(int signal);
void* thread_f(void* argv);
void handle_f(struct client_t client);

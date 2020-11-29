#pragma once

#include "server.h"

using namespace std;

const map<int, string> statuses
{
    pair<int, string>{200, "OK"},
    pair<int, string>{403, "Forbidden"},
    pair<int, string>{404, "Not Found"},
    pair<int, string>{405, "Method Not Allowed"},
};

const map<string, string> content_types
{
    pair<string, string>{".html", "text/html"},
    pair<string, string>{".css", "text/css"},
    pair<string, string>{".js", "application/javascript"},
    pair<string, string>{".jpg", "image/jpeg"},
    pair<string, string>{".jpeg", "image/jpeg"},
    pair<string, string>{".png", "image/png"},
    pair<string, string>{".gif", "image/gif"},
};

string string_to_hex(const string& input);

map<string, string> get_headers(string header_text);

string get_start_response_line(
    string protocol, int status_code, string status_string);

string response_format(
    string protocol, int status_code, string status_string,
    map<string, string> headers, string body);

tuple<string, string, string>
split_start_line(string start_line);

string get_content_type(string extension);
int check_host(map<string, string> headers);
string get_extension(string path);
string get_response(struct client_t client, string request);
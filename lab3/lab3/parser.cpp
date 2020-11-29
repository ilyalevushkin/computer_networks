#include "headers/parser.h"


string string_to_hex(const string& input)
{
    static const char hex_digits[] = "0123456789ABCDEF";

    string output;
    output.reserve(input.length() * 2);
    for (unsigned char c : input)
    {
        output.push_back(hex_digits[c >> 4]);
        output.push_back(hex_digits[c & 15]);
    }

    return output;
}


map<string, string> get_headers(string header_text)
{
    map<string, string> headers;
    istringstream header_list{header_text};
    string line;
    while (getline(header_list, line) && line != "\n")
    {
        auto name_end = line.find(':');

        auto name = line.substr(0, name_end);
        auto value = line.substr(name_end + 2, line.length() - name_end - 1);

        headers[name] = value;
    }
    return headers;
}

string get_start_response_line(
    string protocol, int status_code, string status_string)
{
    auto start_response_line = protocol + " " + to_string(status_code)
        + " " + status_string;
    return start_response_line;
}

string response_format(
    string protocol, int status_code, string status_string,
    map<string, string> headers, string body)
{
    string response;
    auto start_response_line = get_start_response_line(
        protocol, status_code, statuses.at(status_code));
    response += start_response_line + "\n";

    if (status_code != 200) {
        auto response_file = "static/" + std::to_string(status_code) + ".html";
        ifstream infile{ response_file };
        body = string{
            istreambuf_iterator<char>(infile),
            istreambuf_iterator<char>()
        };
        infile.close();
        headers["Content-Type"] = content_types.at(".html");
        headers["Content-Length"] = to_string(body.length());
    }

    string v[3] = {
    "Content-Type",
    "Content-Length",
    "Connection",
    };
    for (const auto& header : v)
    {
        if (headers.find(header) != headers.end())
        {
            response += header + ": " + headers.at(header) + "\n";
        }
    }

    response += "\n" + body;
    cout << start_response_line.c_str() << endl;
    return response;
}

tuple<string, string, string>
split_start_line(string start_line)
{
    auto method_end = start_line.find(' ');
    auto path_end = start_line.find(' ', method_end + 1);

    auto method = start_line.substr(0, method_end);
    auto path = start_line.substr(method_end + 1, path_end - method_end - 1);
    auto protocol = start_line.substr(path_end + 1, start_line.length() - path_end - 2);
    
    if (path[0] == '/' && path.length() != 1)
    {
        path = path.substr(1, path.length() - 1);
    }
    else
    {
        path = "index.html";
    }
    return {method, path, protocol};
}

string get_content_type(string extension)
{
    string content_type;
    if (content_types.find(extension) == content_types.end())
    {
        content_type = "text/plain";
    }
    else
    {
        content_type = content_types.at(extension);
    }
    return content_type;
}

int check_host(map<string, string> headers)
{
    int status = 200;
    if (headers.find("Host") == headers.end())
    {
        status = 404;
    }
    else
    {
        auto host = headers.at("Host");
        auto port = to_string(SERVER_PORT);
        if (host.compare("127.0.0.1:" + port) != 0
            && host.compare("localhost:" + port) != 0
            && host.compare("127.0.0.1:" + port + "\r") != 0
            && host.compare("localhost:" + port + "\r") != 0)
        {
            status = 404;
        }
    }

    return status;
}

string get_extension(string path)
{
    auto dot_pos = path.find('.');
    auto extension = path.substr(dot_pos, path.length() - dot_pos);
    return extension;
}

string get_response(struct client_t client, string request)
{
    string response;
    int status = 200;
    string status_string = "OK";
    map<string, string> response_headers;
    response_headers["Connection"] = "close";
    string body;

    auto start_line_end = request.find('\n');
    auto start_line = request.substr(0, start_line_end);

    cout << "[" << client.ip_addr.c_str() << "]  request: " << start_line.c_str() << endl;

    cout << request << endl;

    cout << "[" << client.ip_addr.c_str() << "] response: ";

    auto headers = get_headers(request.substr(start_line_end + 1, request.length() - start_line_end));
    status = check_host(headers);

    if (status != 200)
    {
        response = response_format(
            "HTTP/1.1", status, statuses.at(status),
            response_headers, body
        );
        return response;
    }

    auto [method, path, protocol] = split_start_line(start_line);

    if (method.compare("GET") != 0 || protocol.compare("HTTP/1.1") != 0)
    {
        status = 405;
        response = response_format(
            protocol, status, statuses.at(status),
            response_headers, body
        );
        return response;
    }

    ifstream infile{path};

    if (!infile.good())
    {
        status = 404;
        response = response_format(
            protocol, status, statuses.at(status),
            response_headers, body
        );
        return response;
    }
    body = string{
        istreambuf_iterator<char>(infile),
        istreambuf_iterator<char>()
    };
    infile.close();

    auto extension = get_extension(path);
    append_statistics(client.ip_addr, extension);

    response_headers["Content-Type"] = get_content_type(extension);
    int idx = response_headers["Content-Type"].find("image");

    if (idx != string::npos)
    {
        body = string_to_hex(body);
    }
    response_headers["Content-Length"] = to_string(body.length());

    response = response_format(
        protocol, status, statuses.at(status),
        response_headers, body
    );

    return response;
}

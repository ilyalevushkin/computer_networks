#include "headers/statistics.h"


void save_statistics_in_txt_file(void)
{
    auto cur_time = std::chrono::system_clock::now();
    time_t convert_time = std::chrono::system_clock::to_time_t(cur_time);

    stringstream file;
    file << "statistics/" << ctime(&convert_time) << ".txt";

    ofstream fout(file.str());
    for (const auto& ip_addr : statistics_map)
    {
        fout << ip_addr.first << endl;
        for (const auto& data : ip_addr.second)
        {
            fout << "\t" << data.first << ": " << data.second << endl;
        }
        fout << endl;
    }
    fout.close();
}


void append_statistics(string ip_addr, string extension)
{
    pthread_mutex_lock(&content_mutex);
    if (statistics_map.find(ip_addr) == statistics_map.end())
    {
        statistics_map[ip_addr][extension] = 1;
    }
    else
    {
        statistics_map[ip_addr][extension]++;
    }
    pthread_mutex_unlock(&content_mutex);
}
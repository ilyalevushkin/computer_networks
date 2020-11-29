CC=g++
SERVER=server.cpp statistics.cpp handler.cpp parser.cpp
CLIENT=client.cpp
FLAGS=-std=c++17
LIBS=-pthread

all: client server

client:
	$(CC) $(FLAGS) $(CLIENT) -o client

server:
	$(CC) $(FLAGS) $(LIBS) $(SERVER) -o server

clean:
	rm client server
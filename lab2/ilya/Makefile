all: client server

client: client.c const.h
	gcc -std=c11 -o client client.c

server: server.c const.h convert.h convert.c
	gcc -std=c11 -o server server.c
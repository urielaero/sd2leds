all:  main.so  
main.so: main.c
	$(CC) -Wall -g -fPIC -shared -o $@ $? -lc
 

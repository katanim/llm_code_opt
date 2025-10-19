# Makefile for the llm_code_opt project

CC = g++
CFLAGS = -Iinclude -std=c++11
SRC = src/main.cpp
OBJ = $(SRC:.cpp=.o)
EXEC = llm_code_opt

all: $(EXEC)

$(EXEC): $(OBJ)
	$(CC) -o $@ $^

%.o: %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJ) $(EXEC)

.PHONY: all clean
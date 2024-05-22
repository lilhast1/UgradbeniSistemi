#!/bin/bash
as -a -g $1.s -o $1.o > $1.lst
ld -g $1.o -o $1
AS=xa
CC=cl65
CFLAGS=-ttelestrat
LDFILES=
ORIX_ROM=roms
BRANCH=master

ifeq ($(CC65_HOME),)
        CC = cl65
        AS = ca65
        LD = ld65
        AR = ar65
else
        CC = $(CC65_HOME)/bin/cl65
        AS = $(CC65_HOME)/bin/ca65
        LD = $(CC65_HOME)/bin/ld65
        AR = $(CC65_HOME)/bin/ar65
endif

all : build
.PHONY : all


build:
	cd tools && python3 retrieveSoftwareOricOrg.py

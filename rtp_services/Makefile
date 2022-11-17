#Modify this to point to the PJSIP location.
PJBASE=/home/jose/Descargas/pjproject

include $(PJBASE)/build.mak

CC      = $(PJ_CC)
LDFLAGS = $(PJ_LDFLAGS)
LDLIBS  = $(PJ_LDLIBS)
CFLAGS  = $(PJ_CFLAGS)
CPPFLAGS= ${CFLAGS}

# If your application is in a file named myapp.cpp or myapp.c
# this is the line you will need to build the binary.
all: siprtp

siprtp_rpi: siprtp.c
	$(CC) -o $@ $< $(CPPFLAGS) $(LDFLAGS) $(LDLIBS)

clean:
	rm -f siprtp.o siprtp
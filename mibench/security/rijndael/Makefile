# rijndael: aes.c aes.h aestab.h aesxam.c Makefile
# 	gcc -static -O3 -o rijndael aes.c aesxam.c

# clean:
# 	rm -rf rijndael output*

rijndael: aes.c aes.h aestab.h aesxam.c Makefile
	gcc -static aes.c aesxam.c -O3 -o rijndael

clean:
	rm -rf rijndael output*
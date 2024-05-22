#include <stdio.h>

int main() 
{
	int N = 48;
	unsigned int a = 0, b = 1, c = 1;
	for (int i = 48; i >= 0; i--) {
		printf("%u\n", a);
		c = b + a;
		a = b;
		b = c;
	}
	return 0;

}
#include <stdio.h>
#include <alloc.h>
#include <stdint.h>

uint64_t private_key;

char msg[] = "I am going to drill a system of holes through our planet, this afternoon, which would allow me to traverse antipodally the globe and, thus, save money on airplane tickets as well as various other transit-related activities. However, in order to not to cause disturbance of neighbouring individuals, I have to decide whether the hole-to-be happens to intersect any internet cables and adjust accordingly. Additionally, a single bit-flip in any relevant memory cell may cause unimaginable horrors and end of our civilization due to unintentional axial tilt change. To avoid this, I relied on performing an all-reduce operation which has been carried out just now. Surely it will be OK.\n";

uint64_t private_val = 10;

int main()
{
	uint32_t i;

	uint32_t *heap = (uint32_t *) pi_malloc(4 * 4444);

	for (i = 0; i < 4444; i++) {
		volatile uint32_t *ptr = (volatile uint32_t *) &heap[i];
		*ptr = i;
	}

	printf("We use the dynamically allocated memory interval [%p - %p]...\n", heap, heap + 4444);

	uint32_t result = 0;

	for (i = 0; i < 4444; i++) {
		uint32_t tmp = *((volatile uint32_t *) &heap[i]);
		result += tmp;
	}

	printf("And perform all-reduce over it saving its value %u to 0x77770!\n", result);

	printf("And we print a large message as well!\n");

	volatile uint32_t *target = (volatile uint32_t *) 0x77770;
	*target = result;

    printf("%s", msg);

	return 0;
}

#include <stdio.h>
#include "ft_printf.h"

int main(void)
{
    int a;
    int b;

    // a = ft_printf("Hello %s %c %d %i %u %x %X %p %%\n",
    //                "42", 'A', -42, -42, 42, 255, 255, NULL);
    // b = printf("Hello %s %c %d %i %u %x %X %p %%\n",
    //            "42", 'A', -42, -42, 42, 255, 255, NULL);

    // printf("ft_printf returned: %d\n", a);
    // printf("printf returned:    %d\n", b);

    ft_printf("\nString:%\n");

    printf("\nString:%\n");
    
    return (0);
}
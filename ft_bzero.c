/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_bzero.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mewaysi <mewaysi@learner.42.tech>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/29 19:10:24 by mewaysi           #+#    #+#             */
/*   Updated: 2025/12/04 12:45:30 by mewaysi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

void	ft_bzero(void *s, size_t n)
{
	unsigned char	*z;

	z = (unsigned char *)s;
	while (n--)
	{
		*z = 0;
		z++;
	}
}

int	main(void)
{
	char	str[10];

	str[10] = "Hello";
	ft_bzero(str, 5);
	printf("%s\n", str);
	return (0);
}

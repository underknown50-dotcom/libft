/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mewaysi <mewaysi@learner.42.tech>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/29 17:32:50 by mewaysi           #+#    #+#             */
/*   Updated: 2025/12/04 12:41:40 by mewaysi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

#include <string.h>

void	*ft_memset(void *ptr, int value, size_t len)
{
	unsigned char	*p;
	unsigned char	v;

	p = (unsigned char *)ptr;
	v = (unsigned char)value;
	while (len--)
	{
		*p++ = v;
	}
	return (ptr);
}

int	main(void)
{
	char	str[10];

	str[10] = "abcdef";
	ft_memset(str, 'X', 3);
	printf("%s\n", str);
	return (0);
}

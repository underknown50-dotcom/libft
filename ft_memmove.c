/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memmove.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mewaysi <mewaysi@learner.42.tech>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/29 19:49:31 by mewaysi           #+#    #+#             */
/*   Updated: 2025/12/04 14:08:18 by mewaysi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>
#include <stddef.h>

void	*ft_memmove(void *dest, const void *src, size_t n)
{
	unsigned char		*d;
	const unsigned char	*s;

	d = (unsigned char *)dest;
	s = (const unsigned char *)src;
	if (d == s || n == 0)
		return (dest);
	if (d < s)
	{
		while (n-- > 0)
			*d++ = *s++;
	}
	else
	{
		d += n;
		s += n;
		while (n-- > 0)
		{
			d--;
			s--;
			*d = *s;
		}
	}
	return (dest);
}

int	main(void)
{
	char	str[7];

	str[0] = '1';
	str[1] = '2';
	str[2] = '3';
	str[3] = '4';
	str[4] = '5';
	str[5] = '6';
	str[6] = '\0';
	ft_memmove(str + 2, str, 4);
	printf("%s\n", str);
	return (0);
}

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isprint.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mewaysi <mewaysi@learner.42.tech>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/25 17:05:41 by mewaysi           #+#    #+#             */
/*   Updated: 2025/11/25 17:57:32 by mewaysi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

int	ft_isprint(int printable)
{
	if (printable >= 32 && printable <= 126)
		return (1);
	else
		return (0);
}
/*
int main ()
{
	printf("f is a %d\n",ft_isprint('f'));
}
*/

/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isalpha.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mewaysi <mewaysi@learner.42.tech>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/11/25 13:45:20 by mewaysi           #+#    #+#             */
/*   Updated: 2025/11/25 17:13:27 by mewaysi          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include <stdio.h>

int	ft_isalpha(int letter)
{
	if ((letter >= 'a' && letter <= 'z') || (letter >= 'A' && letter <= 'Z'))
		return (1);
	else
		return (0);
}
/*int main()
{
	printf("a is %d\n",ft_isalpha('a'));
	printf("A is %d\n",ft_isalpha('Z'));
	printf("3 is %d\n",ft_isalpha('3'));
	printf("= is %d\n",ft_isalpha('='));
	printf("nothing is %d",ft_isalpha(' '));
}
*/

typedef struct s_list
{
void *content;
struct s_list *next;
} t_list;

void    ft_lstiter(t_list *lst, void (*f)(void *))
{
    if (!lst || !f)
    {
        return;
    }
    while (lst)
    {
        f(lst->content);
        lst = lst->next;
    }
}
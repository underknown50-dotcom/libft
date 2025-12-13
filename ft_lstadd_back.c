typedef struct s_list
{
void *content;
struct s_list *next;
} t_list;

void    ft_lstadd_back(t_list **lst, t_list *new)
{
    t_list  *last;

    last = *lst;
    if (!lst || !new)
    {
        return;
    }
    while (!*lst)
    {
        *lst = new;
        return;
    }
    while (last->next)
    {
        last = last->next;
    }
    last->next = new;
}
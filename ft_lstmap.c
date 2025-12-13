typedef struct s_list
{
void *content;
struct s_list *next;
} t_list;

t_list *ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
   t_list *new_list = NULL;
    t_list *tail = NULL;
    t_list *new_node;
    void   *new_content;

    if (!lst || !f || !del)
        return (NULL);

    while (lst != NULL)
    {
        /* أولاً نطبّق f ونتأكد من النتيجة قبل تخصيص النود */
        new_content = f(lst->content);
        if (!new_content)
        {
            /* نحرر كل النودز اللي اننشأت سابقاً */
            while (new_list)
            {
                t_list *tmp = new_list->next;
                del(new_list->content);
                free(new_list);
                new_list = tmp;
            }
            return (NULL);
        }

        /* نخصص النود الجديدة */
        new_node = (t_list *)malloc(sizeof(t_list));
        if (!new_node)
        {
            /* لو malloc فشل، نحرر المحتوى الجديد وننظف القائمة */
            del(new_content);
            while (new_list)
            {
                t_list *tmp = new_list->next;
                del(new_list->content);
                free(new_list);
                new_list = tmp;
            }
            return (NULL);
        }

        new_node->content = new_content;
        new_node->next = NULL;

        /* نربطه بنهاية القايمة الجديدة (نستخدم tail للـ O(1) append) */
        if (!new_list)
        {
            new_list = tail = new_node;
        }
        else
        {
            tail->next = new_node;
            tail = new_node;
        }

        lst = lst->next;
    }

    return (new_list);
}

#include<iostream>

using namespace std;

struct node{
    int data;
    struct node *next;
};

void push(struct node** head, int new_data){
    struct node* new_node = (struct node*) malloc(sizeof(struct node));
    new_node->data = new_data;
    new_node->next = (*head);
    (*head) = new_node;
}

void deleteNode(struct node **head, int key){
    struct node* temp = *head, *prev;

    if (temp != NULL && temp->data == key){
        *head = temp->next;
        free(temp);
        return;
    }

    while (temp != NULL && temp->data != key){
        prev = temp;
        temp = temp->next;
    }

    if (temp == NULL) return;

    prev->next = temp->next;

    free(temp);
}

void printNode(struct node *node){
    while (node != NULL){
        cout << node->data << " ";
        node = node->next;
    }
}

int main(){

    struct node* head = NULL;

    push(&head, 7);
    push(&head, 10);
    push(&head, 15);
    push(&head, 1);
    push(&head, 3);
    push(&head, 2);

    puts("Created Linked List: ");
    printNode(head);
    deleteNode(&head, 15);
    puts("\nLinked List after Deletion position of 15: ");
    printNode(head);
    puts("\n");
    return 0;
}

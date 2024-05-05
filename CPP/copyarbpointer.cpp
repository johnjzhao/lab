#include <bits/stdc++.h>
using namespace std;

struct LinkedListNode{
    int data;
    LinkedListNode *next;
    LinkedListNode *arbit;
};

void free_list(LinkedListNode * head){
    if(!head) return;
    LinkedListNode * temp = head;
    LinkedListNode * next = head;
    while(temp){
        next = temp->next;
        free(temp);
        temp = next;
    }
}

void push(LinkedListNode** head, int value){
    if(*head == NULL){
        (*head) = (LinkedListNode *)malloc(sizeof(LinkedListNode));
        (*head)->data = value;
        (*head)->next = NULL;
    }   
    else{
        LinkedListNode * temp = (LinkedListNode *)malloc(sizeof(LinkedListNode));
        if(temp){
            temp->data = value;
            temp->next = (*head);
            *head = temp;
        }
    }
}

void printNode(LinkedListNode* head){
    cout << head->data << "("
        << head->arbit->data << ")";
    head = head->next;
    while (head != NULL) {
        cout << " -> " << head->data << "("
            << head->arbit->data << ")";
        head = head->next;
    }
    cout << endl;
}

void add_arbit(LinkedListNode *L1, int a, int b){
    LinkedListNode * first = L1;
    LinkedListNode * second = L1;

    while(first){
        if(first->data == a)
            break;
        first = first->next;
    }
    while(second){
        if(second->data == b)
            break;
        second = second->next;
    }
    if(first)
        first->arbit = second;
    }
    LinkedListNode* create_node(int val){

    LinkedListNode* temp =  (LinkedListNode*)malloc(sizeof(LinkedListNode));
    if(temp){
        temp->data = val;
        temp->next = NULL;
    }
    return temp;
}

LinkedListNode* clone(LinkedListNode* node){

    if(!node) return NULL;
    LinkedListNode* current = node;

    while(current){
        LinkedListNode* current_next = current->next;
        current->next  =  create_node(current->data);
        current->next->next = current_next;
        current = current_next;
    }   
    current = node;

    LinkedListNode* clone_head  = current->next;
    while(current){
        LinkedListNode * clone = current->next;
        if(current->arbit){
            clone->arbit    = current->arbit->next;
        }
        current = clone->next;
    }

    current = node;

    while(current){
        LinkedListNode* clone  = current->next;
        current->next = clone->next;
        if(clone->next){
            clone->next = clone->next->next;
        }
        current = current->next;
    }
    return clone_head;
    }

int main(){
    LinkedListNode* L1 = NULL;
    push(&L1,11);
    push(&L1,2);
    push(&L1,7);
    push(&L1,4);
    push(&L1,5);
    push(&L1,6);

    add_arbit(L1,11,6);
    add_arbit(L1,2,5);
    add_arbit(L1,7,11);
    add_arbit(L1,4,2);
    add_arbit(L1,5,4);
    add_arbit(L1,6,7);

    puts("Created Linked List: ");
    printNode(L1);
    LinkedListNode *clone_head  = clone(L1);
    puts("\nLinked List after clone: ");
    printNode(L1);
    puts("\n");
    free_list(L1);

    return 0;    
} 


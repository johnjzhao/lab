#include <bits/stdc++.h>
using namespace std;

struct LinkedListNode {
	int data;
	LinkedListNode* next;
	LinkedListNode* arbit;

	LinkedListNode(int x){
		this->data = x;
		this->next = NULL;
		this->arbit = NULL;
	}
};

LinkedListNode* copyArbPointer(LinkedListNode* head){

	unordered_map<LinkedListNode*, LinkedListNode*> mp;
	LinkedListNode *temp, *nhead;

	temp = head;
	nhead = new LinkedListNode(temp->data);
	mp[temp] = nhead;

	while (temp->next != NULL) {
		nhead->next 
			= new LinkedListNode(temp->next->data);
		temp = temp->next;
		nhead = nhead->next;
		mp[temp] = nhead;
	}
	temp = head;

	while (temp != NULL) {
		mp[temp]->arbit = mp[temp->arbit];
		temp = temp->next;
	}

	return mp[head];
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

int main(){

	LinkedListNode* head = new LinkedListNode(1);
	head->next = new LinkedListNode(2);
	head->next->next = new LinkedListNode(3);
	head->next->next->next = new LinkedListNode(4);
	head->next->next->next->next 
		= new LinkedListNode(15);
	head->arbit = head->next->next;
	head->next->arbit = head;
	head->next->next->arbit 
		= head->next->next->next->next;
	head->next->next->next->arbit 
		= head->next->next;
	head->next->next->next->next->arbit 
		= head->next;

	cout << "The original linked list:\n";
	printNode(head);

	LinkedListNode* sol = copyArbPointer(head);

	cout << "The cloned linked list:\n";
	printNode(sol);

	return 0;
}

#include<iostream>

using namespace std;

LinkedListNode* deep_copy_arbitrary_pointer(
    LinkedListNode* head) {

  if (head == nullptr) {
    return nullptr;
  }

  LinkedListNode* current = head;
  LinkedListNode* new_head = nullptr;
  LinkedListNode* new_prev = nullptr;
  unordered_map<LinkedListNode*, LinkedListNode*> map;

  // create copy of the linked list, recording the corresponding
  // nodes in hashmap without updating arbitrary pointer
  while (current != nullptr) {
    LinkedListNode* new_node = 
      new LinkedListNode(current->data);

    // copy the old arbitrary pointer in the new node
    new_node->arbitrary_pointer = current->arbitrary_pointer;

    if (new_prev != nullptr) {
      new_prev->next = new_node;
    }
    else {
      new_head = new_node;
    }

    map[current] = new_node;

    new_prev = new_node;
    current = current->next;
  }

  LinkedListNode* new_current = new_head;

  // updating arbitrary_pointer
  while (new_current != nullptr) {
    if (new_current->arbitrary_pointer != nullptr) {
      LinkedListNode* node = 
        map[new_current->arbitrary_pointer];
      new_current->arbitrary_pointer = node;
    }

    new_current = new_current->next;
  }

  return new_head;
}

LinkedListNode* create_linked_list_with_arb_pointers(int length) {
  LinkedListNode* head = LinkedList::create_random_list(length);
  vector<LinkedListNode*> v;
  LinkedListNode* temp = head;
  while (temp) {
    v.push_back(temp);
    temp = temp->next;
  }

  for (size_t i = 0; i < v.size(); ++i) {
    int j = rand() % v.size();
    int p = rand() % 100;
    if ( p < 75) {
      v[i]->arbitrary_pointer = v[j];
    }
  }

  return head;
}

void print_with_arb_pointers(LinkedListNode* head) {
  while (head != nullptr) {
    cout << head->data << " (";
    if (head->arbitrary_pointer)
      cout << head->arbitrary_pointer->data;
    cout << "), ";
    head = head->next;
  }
  cout << endl;
}

// Test Program.
int main() {
  LinkedListNode* head = create_linked_list_with_arb_pointers(15);
  print_with_arb_pointers(head);

  LinkedListNode* head2 = deep_copy_arbitrary_pointer(head);
  print_with_arb_pointers(head2);

  return 0;
}

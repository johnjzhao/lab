#include<bits/stdc++.h>
using namespace std;
struct Node {
   int data;
   struct Node* left;
   struct Node* right;
};
struct Node* newNode(int data) {
   struct Node* node = new Node;
   node->data = data;
   node->left = NULL;
   node->right = NULL;
   return node;
}
void convertTreeToItsMirror(struct Node* node) {
   if (node == NULL) {
      return;
   }
   else {
      struct Node* temp;
      convertTreeToItsMirror(node->left);
      convertTreeToItsMirror(node->right);
      temp = node->left;
      node->left = node->right;
      node->right = temp;
   }
}
void printTree(struct Node* node) {
   if (node == NULL) {
      return;
   }
   printTree(node->left);
   cout << node->data << " ";
   printTree(node->right);
}
int main() {
   struct Node *root = newNode(1);
   root->left = newNode(2);
   root->right = newNode(3);
   root->left->left = newNode(4);
   root->left->right = newNode(5);
   cout << "The original Tree: \n ";
   printTree(root);
   cout << endl;
   convertTreeToItsMirror(root);
   cout << "Mirror of the Tree:\n ";
   printTree(root);
   cout << endl;
   return 0;
}

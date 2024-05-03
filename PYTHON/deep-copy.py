import random

class Node:
	def __init__(self,data):
		self.data = data
		self.next = None

class Singly_Linked_List:
	def __init__(self):
		self.head = None
		self.tail = None

	def insert_at_last(self,data):
		new_node = Node(data)

		if self.head == None:
			self.head = new_node
			self.tail = new_node
		else:
			self.tail.next = new_node
			self.tail = new_node

	def print_Singly_Linked_List(self):
		t_head = self.head
		print("\n Our Singly_Linked_List is : ",end="")
		while(t_head):
			print(t_head.data,end=" -> ")
			t_head = t_head.next
		print("Null \n")

start = 0
end = 20
random_int = lambda : random.randint(start,end)


def main():
	linked_list = Singly_Linked_List()
	for i in range(random_int()):
		linked_list.insert_at_last(i)
	
	linked_list.print_Singly_Linked_List()


if __name__ == "__main__":
	main()


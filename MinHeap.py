#import Node

class MinHeap:
    def __init__(self):
        self.length = 0;
        self.elements = [];

    #def __init__(self, array):
    #    self.length = len(array);
    #    self.elements  = array[:];

    def BuildMinHeap(self):
        for index in range((self.length-1)/2, 0, -1):
            TopDownHeapify(index);

    def TopDownHeapify(self, index):
        l_child_index = 2*index + 1;
        r_child_index = 2*index + 2;
        if l_child_index >= self.length:
            return;

        child = self.elements[l_child_index].GetKey();
        child_index = l_child_index;
        if r_child_index < self.length:
            r_child_val = self.elements[r_child_index].GetKey();
            if r_child_val < child :
                child = r_child_val;
                child_index = r_child_index;
        if self.elements[index].GetKey() > child:
            self.swap(index, child_index);
        self.TopDownHeapify(child_index);

    def BottomTopHeapify(self, index):
        if index == 0:
            return;
        parent_index = (index-1)/2;
        parent_val = self.elements[parent_index].GetKey();
        if self.elements[index].GetKey() < parent_val:
            self.swap(index, parent_index);
            self.BottomTopHeapify(parent_index);

    def swap(self, index1, index2):
        temp = self.elements[index1];
        self.elements[index1] = self.elements[index2];
        self.elements[index2] = temp;

    def pop(self):
        head = self.elements[0];
        self.length -= 1;
        self.elements[0] = self.elements[self.length];
        self.elements.pop();
        self.TopDownHeapify(0);
        return head;

    def AddElements(self, node):
        self.elements.append(node);
        self.length += 1;
        self.BottomTopHeapify(self.length - 1);

    def PrintElements(self):
        for i in range(self.length):
            print self.elements[i].GetValue() , ' , ' , ;

    def AddAtHead(self, node):
        self.elements[0] = node;
        self.TopDownHeapify(0);

    def ReturnHead(self):
        return self.elements[0];

    def GetSize(self):
        return self.length;

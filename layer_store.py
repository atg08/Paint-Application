from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer , LAYERS , get_layers
from layers import invert, lighten , darken
from data_structures.queue_adt import CircularQueue
from data_structures.stack_adt import ArrayStack
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem



class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass



class SetLayerStore(LayerStore):

    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    # status of application of special mode and initialising it to OFF - False
    
    is_special = False

    # implementing abstract methods given

    def __init__(self) -> None:

        """
        defining the magic method : __init__ 
        - This initialises an object of the SetLayerStore class; Initialised to None (no LayerStore applied)

        Args:
        - self
        
        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(1)
        - Best case: O(1) 
        """

        self.my_layer = None
   

    def add(self, layer: Layer) -> bool:

        """
        Adds the specified input layer to the store.
    
        Args:
        - self
        - layer of Layer class

        Raises:
        - None

        Returns:
        - boolean value True if the LayerStore was actually changed (if a layer was added) 
        - boolean value False if LayerStore was not changed (when the input layer is the same as the current layer in the store)
        

        Complexity:
        - Worst case: O(comp) where comp is the complexity of comparision
        - Best case: O(comp)
        """

        if self.my_layer != layer:
            self.my_layer = layer
            return True

        #else returns false as it is the same layer and we dont need to reassign
        return False

    
    def get_color(self, start : tuple[int, int, int], timestamp : int, x : int, y : int) -> tuple[int, int, int]:

        """
        - Returns the colour this square should show, given the current layer
        - If there is no layer, the input colour (start) is returned
        - If special is applied, the inverted colour is returned

        Args:
        - self
        - start : a tuple with integers, containing the background layer
        - timestemp : interger value
        - x : interger value where x is the coloumn index of the square
        - y : interger value where y is the row index of the square

        Raises:
        - None

        Returns:
        - Returns the colour this square should show, given the current layer
        - If there is no layer, the input colour (start) is returned
        - If special is applied, the inverted colour is returned

        Complexity:
        - Worst case: O(comp . other_function) 
        - Best case: O(comp . other_function)
        """

        temp_original_colour = start

        # using apply function to get colour
        if self.my_layer != None:
            temp_original_colour = self.my_layer.apply(temp_original_colour, timestamp, x, y)   
    
        
        #condition when special fuction is true i.e. selected to invert colours 

        if self.is_special == True: 
            temp_inverted_colour = []  
            for i in range(0,len(temp_original_colour)):
                temp_inverted_colour.append(255 - temp_original_colour[i]) 
            temp_inverted_colour = tuple(temp_inverted_colour)

            return temp_inverted_colour

        else:
            return temp_original_colour


    def erase(self, layer: Layer) -> bool:

        """
        Erases the current layer in the store.
        - The input parameter layer is ignored
    
        Args:
        - self
        - layer of Layer class

        Raises:
        - None

        Returns:
        - boolean value True if the LayerStore was actually changed (if the current layer was removed/erased) 
        - boolean value False if LayerStore was not changed (when no layer is applied currently)
        

        Complexity:
        - Worst case: O(comp) where comp is the complexity of comparision
        - Best case: O(comp)
        """
        
        if self.my_layer != None:
            self.my_layer = None
            return True
        
        #returns false as the layer is already set to none i.e. there is no layer assigned 
        return False


    def special(self):
        """
        Toggles the application of special mode on the square, which in this layer inverts the colour
    
        Args:
        - self

        Raises:
        - None

        Returns:
        - None 
        
        Complexity:
        - Worst case: O(1) 
        - Best case: O(1)
        """

        self.is_special = not self.is_special 


        
class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self) -> None:

        """
        defining the magic method : __init__ 
        - This initialises an object of the AdditiveLayerStore class; 
        - Data structure ArraySortedList is used to store the list of applied layers
        - Counter is a unique key for Listitem used in ArraySortedList. It is incremented by 1 when a new layer is added to the LayerStore 

        Args:
        - self
        
        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(other_function)
        - Best case: O(other_function) 
        """

        temp_len = 100 * (len(get_layers()))

        self.my_layer_list = ArraySortedList(temp_len)
        self.counter = 0
        
 
    def add(self, layer: Layer) -> bool:
        """
        Add the input layer to the store.
        - Creates an instace of Listitem using the input layer as value and the current counter as the key; Adds that to the list
        - Increments the counter by 1
    
        Args:
        - self
        - layer of Layer class

        Raises:
        - None

        Returns:
        - boolean value True when the LayerStore was actually changed , i.e. the input layer was added
        
        Complexity:
        - Worst case: O(other_function) where other_function is the complexity of add
        - Best case: O(other_function)
        """

        temp_listitem = ListItem(layer , self.counter)
        self.my_layer_list.add(temp_listitem)
        self.counter = self.counter + 1

        return True


    def get_color(self, start : tuple[int, int, int], timestamp : int, x : int, y : int) -> tuple[int, int, int]:

        """
        - Returns the colour this square should show 
        - The collection of layers from the list are applied one-by-one, from earliest added to latest added
        - If there is no layer, the input colour (start) is returned

        Args:
        - self
        - start : a tuple with integers, containing the background layer
        - timestemp : interger value
        - x : interger value where x is the coloumn index of the square
        - y : interger value where y is the row index of the square

        Raises:
        - None

        Returns:
        - The final colour of the combination of layers is returned 
        - If there is no layer, the input colour (start) is returned

        Complexity:
        - Worst case: O(other_function . len(self.my_layer_list))
        - Best case: O(other_function . len(self.my_layer_list))
        """

        temp_colour = start

        if not self.my_layer_list.is_empty():
            for list_index in range (len(self.my_layer_list)):
                temp_layer = self.my_layer_list[list_index].value
                temp_colour = temp_layer.apply(temp_colour, timestamp, x, y)
        
        return temp_colour

 
    def erase(self, layer: Layer) -> bool:

        """
        Erases the oldest layer (the first input layer) in the store 
        - The input parameter layer is ignored
    
        Args:
        - self
        - layer of Layer class

        Raises:
        - None

        Returns:
        - boolean value True when the layer at index 0 is removed/erased (oldest layer by age)
        - boolean value False if the list is empty i,e, there is nothing to erase
        

        Complexity:
        - Worst case: O(other_function) where other_function is the complexity of is.empty and delete_at_index
        - Best case: O(other_function)
        """

        if self.my_layer_list.is_empty():
            return False

        self.my_layer_list.delete_at_index(0)
        return True

   
    def special(self):

        """
        Special mode in AdditiveLaterStore reverses the ages of all the input layers 
        (i.e. the oldest layer becomes the youngest and so on)
        - The value of the Listitem with the smallest key is switched with the value of the Listitem with the largest key and so on
    
        Args:
        - self

        Raises:
        - None

        Returns:
        - None 
        
        Complexity:
        - Worst case: O(len(self.my_layer_list) // 2) 
        - Best case: O(len(self.my_layer_list) // 2)
        """

        if self.my_layer_list.is_empty():
            return
        
        for list_index in range (len(self.my_layer_list) // 2):
            temp_listitem_layer = self.my_layer_list[list_index].value
            self.my_layer_list[list_index].value = self.my_layer_list[len(self.my_layer_list) - 1 - list_index].value
            self.my_layer_list[len(self.my_layer_list) - 1 - list_index].value = temp_listitem_layer



class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self) -> None:

        """
        defining the magic method : __init__ 
        - This initialises an object of the SequenceLayerStore class; 
        - Data structure ArraySortedList is used to keep track of every layer as "applying" or "not applying"; which is the value of the Listitem
        - The key of the Listitem is the index of the corresponding layer in LAYERS

        Args:
        - self
        
        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(temp_length . comp . other_function)
        - Best case: O(temp_length . comp . other_function) 
        """

        temp_length = len(get_layers())
        self.my_layer_list = ArraySortedList(temp_length)

        temp_apply_status = False

        for layer_index in range(temp_length):
            if LAYERS[layer_index] != None:
                temp_listitem = ListItem(temp_apply_status, layer_index)
                self.my_layer_list.add(temp_listitem)
                

    def add(self, layer: Layer) -> bool:

        """
        Changes the input layer to True or "applying" if it not applied already
    
        Args:
        - self
        - layer of Layer class

        Raises:
        - None

        Returns:
        - boolean value True when the LayerStore was actually changed , i.e. the status of the layer was changed to True - "applying"
        - boolean value False if the list is empty or if the input layer already exists

        Complexity:
        - Worst case: O(comp + (len(LAYERS) . comp . comp . comp))
        - Best case: O(comp + (len(LAYERS) . comp . comp . comp))
        """

        if len(self.my_layer_list) == 0:
            return False

        for layer_index in range(len(LAYERS)):
            if LAYERS[layer_index] != None:
                if layer.name == LAYERS[layer_index].name:
                    temp_listitem = self.my_layer_list[layer_index]

                    if temp_listitem.value == True:
                        return False

                    self.my_layer_list[layer_index].value = True
                    return True



    def get_color(self, start : tuple[int, int, int], timestamp : int, x :int, y : int) -> tuple[int, int, int]:

        """
        - Iterates over the list and checks if a layer is added 
        - The colour of the Layer store is calculated by applying each Layer which is currently "applying", in order based on their index (accessible through layer.index)
        - Otherwise the input colour (start) is returned

        Args:
        - self
        - start : a tuple with integers, containing the background layer
        - timestemp : interger value
        - x : interger value where x is the coloumn index of the square
        - y : interger value where y is the row index of the square

        Raises:
        - None

        Returns:
        - If there is no layer, the input colour (start) is returned
        - If a layer is True - "applying", returns the colour of the layer applied

        Complexity:
        - Worst case: O(comp . len(LAYERS) . comp . comp . other_function) 
        - Best case: O(comp . len(LAYERS) . comp . comp . other_function)
        """

        temp_colour = start

        if len(self.my_layer_list) > 0:
            for layer_index in range (len(LAYERS)):
                if LAYERS[layer_index] != None:
                    temp_listitem = self.my_layer_list[layer_index]

                    if temp_listitem.value == True:
                        temp_colour = LAYERS[layer_index].apply(temp_colour, timestamp, x, y)

        return temp_colour


    
    def erase(self, layer: Layer) -> bool:
        """
        Changes the input layer to False or "not applying" 
    
        Args:
        - self
        - layer of Layer class

        Raises:
        - None

        Returns:
        - boolean value True when the LayerStore was actually changed , i.e. the status of the layer was changed to False - "not applying"
        - boolean value False if the list is empty or if the input layer does not exist
        

        Complexity:
        - Worst case: O(comp + (len(LAYERS) . comp . comp . comp) 
        - Best case: O(comp + (len(LAYERS) . comp . comp . comp)
        """

        if len(self.my_layer_list) == 0:
            return False

        for layer_index in range(len(LAYERS)):
            if LAYERS[layer_index] != None:
                if layer.name == LAYERS[layer_index].name:
                    temp_listitem = self.my_layer_list[layer_index]

                    if temp_listitem.value == False:
                        return False

                    self.my_layer_list[layer_index].value = False
                    return True
        
    
    def special(self):

        """
        Special mode in SequenceLaterStore removes the median "applying" layer based on its name, lexicographically ordered in LAYERS, 
        in the case of an even number of applying layers, select the lexicographically smaller of the two names.
         
        Args:
        - self

        Raises:
        - None

        Returns:
        - None 
        
        Complexity:
        - Worst case: O(comp + (len(LAYERS) . comp . comp . other_function) + comp + comp + (len(LAYERS) . comp .comp))
        - Best case: O(comp + (len(LAYERS) . comp . comp . other_function) + comp + comp + (len(LAYERS) . comp .comp))
        """
       
        if len(self.my_layer_list) > 0:
            temp_sorted_list = ArraySortedList(len(LAYERS))
            for layer_index in range(len(LAYERS)):
                if LAYERS[layer_index] != None:
                    temp_listitem = self.my_layer_list[layer_index]

                    if temp_listitem.value == True:
                        temp_listitem_name = ListItem(False, LAYERS[layer_index].name)
                        temp_sorted_list.add(temp_listitem_name)


            index_to_delete = 0
            if len(temp_sorted_list) == 0:
                return

            if len(temp_sorted_list) % 2 != 0:
                index_to_delete = (len(temp_sorted_list) // 2) 

            else:
                index_to_delete = (len(temp_sorted_list) // 2) - 1

            name_to_delete = temp_sorted_list[index_to_delete].key

            for layer_index in range(len(LAYERS)):
                if LAYERS[layer_index] != None:
                    if name_to_delete == LAYERS[layer_index].name:
                        self.my_layer_list[layer_index].value = False

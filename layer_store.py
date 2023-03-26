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

    # indicating status of special mode and initialising it to OFF
    
    is_special = False

    # implementing abstract methods given

    def __init__(self) -> None:
        self.my_layer = None
   

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """

        if self.my_layer != layer:
            self.my_layer = layer
            return True

        #else returns false as it is the same layer and we dont need to reassign
        return False

    
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        temp_original_colour = start

        # using apply function to get colour
        if self.my_layer != None:
            temp_original_colour = self.my_layer.apply(start, timestamp, x, y)
    
        #print("original colour is " , original_colour , " X and Y are ", x, y)
        
        #condition when special fuction is true i.e. selected to invert colours 

        if self.is_special == True:
            temp_inverted_colour=[]  
            for i in range(0,len(temp_original_colour)):
                temp_inverted_colour.append(255 - temp_original_colour[i])
            temp_inverted_colour = tuple(temp_inverted_colour)

            #print("inverted colour is " , inverted_colour)
            return temp_inverted_colour

        else:
            return temp_original_colour


    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        if self.my_layer != None:
            self.my_layer = None
            return True
        
        #returns false as the layer is already set to none i.e. there is no layer assigned 
        return False


    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        #toggles the special mode for that layer

        self.is_special = not self.is_special


        
class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self) -> None:

        temp_len = 100 * (len(get_layers()))

        self.my_layer_list = ArraySortedList(temp_len)
        self.counter = 0
        
 
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """

        temp_listitem = ListItem(layer , self.counter)
        self.my_layer_list.add(temp_listitem)
        self.counter = self.counter + 1

        return True


    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        temp_colour = start

        if not self.my_layer_list.is_empty():
            for list_index in range (len(self.my_layer_list)):
                temp_layer = self.my_layer_list[list_index].value
                temp_colour = temp_layer.apply(temp_colour, timestamp, x, y)
        
        return temp_colour

 
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """

        if self.my_layer_list.is_empty():
            return False

        self.my_layer_list.delete_at_index(0)
        return True

   
    def special(self):
        """
        Special mode. Different for each store implementation.
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

        temp_length = len(get_layers())
        self.my_layer_list = ArraySortedList(temp_length)

        temp_apply_status = False

        for layer_index in range(temp_length):
            if LAYERS[layer_index] != None:
                temp_listitem = ListItem(temp_apply_status, layer_index)
                self.my_layer_list.add(temp_listitem)
                

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
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



    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
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
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
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
        Special mode. Different for each store implementation.
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

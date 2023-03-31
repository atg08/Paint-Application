from __future__ import annotations
from data_structures.referential_array import ArrayR
from layer_store import LayerStore
from layer_store import SetLayerStore , AdditiveLayerStore , SequenceLayerStore
from layer_util import get_layers


class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0


    def __init__(self, draw_style : DRAW_STYLE_OPTIONS, x : int, y : int) -> None:
        
        """
        Defining the magic method : __init__ 
        - This initialises an object of the Grid class 
            1. initialises the instance variables based on the input parameters
            2. creates an instance of a LayerStore for each grid square based on the draw style

        Args:
        - self
        - draw style that is one of set, add or sequence - (DRAW_STYLE_OPTIONS)
        - x - number of coloumns in the grid
        - y - number of rows in the grid

        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(y . (x . comp)), where x is the number of coloumns, y is the number of rows and comp is the complexity of comparision 
        - Best case: O(y . (x . comp)), same as worst case since we need to iterate over all the elements in the list
        """

        self.num_of_cols = x
        self.num_of_rows = y
        self.my_draw_style = draw_style
        self.brush_size = self.DEFAULT_BRUSH_SIZE

        self.store_array = ArrayR(self.num_of_rows)

        for row_index in range(self.num_of_rows):
            temp_layer_store_array = ArrayR(self.num_of_cols)
            self.store_array[row_index] = temp_layer_store_array

            for col_index in range(self.num_of_cols):
                if self.my_draw_style == self.DRAW_STYLE_SET:
                    temp_layer_store=SetLayerStore()
                elif self.my_draw_style == self.DRAW_STYLE_ADD:
                    temp_layer_store = AdditiveLayerStore()
                elif self.my_draw_style == self.DRAW_STYLE_SEQUENCE:
                    temp_layer_store = SequenceLayerStore()
                    

                temp_layer_store_array[col_index] = temp_layer_store


    
    def __getitem__(self, Index : int) -> LayerStore:
        """
        defining magic method (__getitem__) 
        - grid[x][y] returns the LayerStore corresponding to the grid square (x, y)
        - (__getitem__ (x)).__getitem__(y) of ArrayR


        Args:
        - self
        - Index - an integer 

        Raises:
        - None

        Returns:
        - The item from store_array with the index of Index

        Complexity:
        - Worst case: O(1)
        - Best case: O(1)
        """

        return self.store_array[Index]
                
                
    def increase_brush_size(self):

        """
        Increases the paint brush size by 1 and does not exceed the maximum brush size: MAX_BRUSH

        Args:
        - self
        
        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(comp), where comp is the complexity of comparision 
        - Best case: O(comp), 
        """

        if self.brush_size < self.MAX_BRUSH:
            self.brush_size = self.brush_size + 1


    def decrease_brush_size(self):
        
        """
        Decreases the brush size by 1 and does not go below the minimum brush size: MIN_BRUSH

        Args:
        - self
        
        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(comp), where comp is the complexity of comparision 
        - Best case: O(comp), 
        """

        if self.brush_size > self.MIN_BRUSH:
            self.brush_size = self.brush_size - 1


    def special(self):
        
        """
        Applies the special effect by calling special() on the LayerStore of each square of the grid

        Args:
        - self
        
        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(x . y . other_function), where x is the number of coloumns, y is the number of rows 
        - Best case: O(x . y . other_function), same as worst case since we need to iterate over all the elements in the list 
        """

        for row_index in range(self.num_of_rows):
            for col_index in range(self.num_of_cols):      
                self.store_array[row_index][col_index].special()






                
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


    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        self.num_of_cols = x
        self.num_of_rows = y
        self.my_draw_style = draw_style
        self.brush_size = self.DEFAULT_BRUSH_SIZE

        #The Grid class should create one instance of the LayerStore for each grid square

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

    
    # These layer stores are accessible by entering grid[x][y]
    
    def __getitem__(self,Index:int) -> LayerStore:
        return self.store_array[Index]
                
                
    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        if self.brush_size < self.MAX_BRUSH:
            self.brush_size = self.brush_size + 1


    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        if self.brush_size > self.MIN_BRUSH:
            self.brush_size = self.brush_size - 1


    def special(self):
        """
        Activate the special affect on all grid squares.
        """

        for row_index in range(self.num_of_rows):
            for col_index in range(self.num_of_cols):      
                self.store_array[row_index][col_index].special()






                
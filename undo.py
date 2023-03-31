from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:

    MAX_CAPACITY = 10000

    def __init__(self) -> None:
        """
        defining the magic method : __init__ 
        - This initialises an object of the Undotracker class; 
        - The data structure used is ArrayStack
        - Two stacks are declared to keep track of the actions to be undone/redone

        Args:
        - self
        
        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(other_function) where other_function is complexity of initialising the ArrayStack
        - Best case: O(other_function) 
        """

        self.my_undo_stack = ArrayStack(self.MAX_CAPACITY)
        self.my_redo_stack = ArrayStack(self.MAX_CAPACITY)

    def clear_undo(self) -> None:

        """
        Completely empties the undo and redo stacks

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

        self.my_undo_stack.clear()
        self.my_redo_stack.clear()
        

    def add_action(self, action: PaintAction) -> None:

        """
        - Adds/pushes the input action into the undo stack and 
        - Clears the redo stack since adding a new action moves the UndoTracker into a different branch, 
           thus the actions in the redo stack become irrelevant
        
        Args:
        - self
        - action of PaintAction class
        
        Raises:
        - None

        Returns:
        - None

        Complexity:
        - Worst case: O(other_function)
        - Best case: O(other_function) 
        """
        
        if not self.my_undo_stack.is_full():
            self.my_undo_stack.push(action)
            self.my_redo_stack.clear()



    def undo(self, grid: Grid) -> PaintAction|None:

        """
        - Pops the top most action from the undo stack and the undone action is applied on the grid
        - Adds the action that was popped, into the redo stack

        Args:
        - self
        - grid of Grid class
        
        Raises:
        - None

        Returns:
        - The top most action of the undo stack
        - None if the undo stack is empty or if the redo stack is full

        Complexity:
        - Worst case: O(other_function)
        - Best case: O(other_function) 
        """

        if self.my_undo_stack.is_empty():
            return None

        if not self.my_redo_stack.is_full():
            temp_action = self.my_undo_stack.pop()
            self.my_redo_stack.push(temp_action)
        
            temp_action.undo_apply(grid)
                    
            return temp_action

        return None


    def redo(self, grid: Grid) -> PaintAction|None:

        """
        - Pops the top most action from the redo stack and the redone action is applied on the grid
        - Adds the action that was popped, into the undo stack
        
        Args:
        - self
        - grid of Grid class
        
        Raises:
        - None

        Returns:
        - The top most action of the redo stack
        - None if the redo stack is empty or if the undo stack is full

        Complexity:
        - Worst case: O(other_function)
        - Best case: O(other_function) 
        """

        if self.my_redo_stack.is_empty():
            return None

        if not self.my_undo_stack.is_full():
            temp_action = self.my_redo_stack.pop()
            self.my_undo_stack.push(temp_action)
        
            temp_action.redo_apply(grid)
        
            return temp_action

        return None


   

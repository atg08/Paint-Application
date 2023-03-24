from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:

    MAX_CAPACITY = 10000

    def __init__(self) -> None:
        self.my_undo_stack = ArrayStack(self.MAX_CAPACITY)
        self.my_redo_stack = ArrayStack(self.MAX_CAPACITY)

    def clear_undo(self) -> None:
        self.my_undo_stack.clear()
        self.my_redo_stack.clear()
        

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        if not self.my_undo_stack.is_full():
            self.my_undo_stack.push(action)



    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
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
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.
        """

        if self.my_redo_stack.is_empty():
            return None

        if not self.my_undo_stack.is_full():
            temp_action = self.my_redo_stack.pop()
            self.my_undo_stack.push(temp_action)
        
            temp_action.redo_apply(grid)
        
            return temp_action

        return None


   

from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import CircularQueue

class ReplayTracker:

    MAX_CAPACITY = 10000

    my_start_replay = False 

    def __init__ (self) -> None:
        
        self.my_replay_queue = CircularQueue(self.MAX_CAPACITY)

    def clear_replay (self) -> None:
        self.my_replay_queue.clear()


    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.
        """
        self.my_start_replay = True


    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.
        """
        if self.my_start_replay == False:
            self.my_replay_queue.append((action , is_undo))

        

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.
        """

        if self.my_replay_queue.is_empty():
            self.my_start_replay = False
            return True

        temp_tuple = self.my_replay_queue.serve()
        temp_paint_action = temp_tuple [0]
        temp_flag = temp_tuple [1]

        if temp_flag == False:
            temp_paint_action.redo_apply(grid)

        else:
            temp_paint_action.undo_apply(grid)

        #print("size of queue in replay next action " , len(self.my_replay_queue))
        return False
        

if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)


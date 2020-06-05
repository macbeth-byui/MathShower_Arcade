# Overview

MathShower is a simple math game implemented using Python Arcade. 

# Instructions

To run this program:

1. Need to install Python 3.x
2. Need to install Arcade (`pip install arcade`)
3. Run: `python mathshower.py`
4. Problems will display at the top of the screen.  Catch the right answer and get points; catch the wrong answer and lose points.  Snowflakes give bonus points and lightning gives penalties.

To create new problems, inherit the `Problem` class.  You will need to modify `create_problem` to create objects of your new problems. You will need to provide values for `self.problem_text`, `self.points_right`, and `self.points_wrong` (which are `None` and 0, respectively in the base class).  You will also need to implement the `solve` function.  The `solve` function will receive a response which you must evaluate and then return the appropriate points.

To create new precipitation, inherit the `Precip` class.  You will need to modify `create_precip` to create objects of your new problems.  The `Precip` class inherits the `arcade.Sprite` class.  At a minimum, you need to provide a value for `self.texture` (which is `None` in the base class) and an implementation for the `hit` function.  The `hit` function will receive a `problem` object for which you may need to call `solve` function on the `problem` object to get the points.

# Useful Links

https://arcade.academy/


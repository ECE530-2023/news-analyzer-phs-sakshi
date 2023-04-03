import threading


class Thread(threading.Thread):
    """
    A wrapper class for threading.Thread which takes as input a function,
    function arguments, callback arguments, and callback function arguments.
    When the thread finishes, it calls the callback function with the output
    of the function as an argument.
    """
    def __init__(self, func, func_args, callback, callback_args):
        super(Thread, self).__init__()
        self.func = func
        self.func_args = func_args
        self.callback = callback
        self.callback_args = callback_args
        self.stop_event = threading.Event()
        self.running = True

    def run(self):
        while self.running:

            # Run the function with the provided arguments
            result = self.func(*self.func_args)
            # Call the callback function with the result and provided arguments
            self.callback(result, *self.callback_args)
            if self.stop_event.is_set():
                self.running = False
                break


    def stop(self):
        """Stop the thread"""
        self.running = False
        self.stop_event.set()

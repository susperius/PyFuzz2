class Worker:
    def start_worker(self):
        raise NotImplementedError("ABSTRACT METHOD")

    def stop_worker(self):
       raise NotImplementedError("ABSTRACT METHOD")
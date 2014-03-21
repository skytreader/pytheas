class Fetcher(object):
    
    def fetch(self):
        """
        Fetch from whatever data store. Returns the appropriate object
        rerpesentation of the fetched data.
        """
        raise NotImplementedError("This fetcher has not yet implemented this method.")

class Sender(object):
    
    def send(self, data):
        """
        Sends the data provided as argument to wherever route.
        """
        raise NotImplementedError("This sender has not yet implemented this method.")



class GeneratorBase:

    chain = None
    device = None
    DEVICE = None
    
    id = None
    title = None
    settings = None
    output_filename = None
    output_path = None

    def load_models(self):
        return None
            
    def do_run(self):
        return self.output_filename

    def __init__(self,chain):
        self.chain = chain
        self.DEVICE = self.chain.DEVICE
        self.device = self.chain.device

    # gc.collect()
    # do_run()

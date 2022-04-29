

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

    def json_override(self,base, new):
        if isinstance(base, dict):
            for k, v in new.items():
                if k in base:
                    base[k] = v
            return {k: self.json_override(v, new) for k, v in base.items()}
        else:
            return base
        
    # gc.collect()
    # do_run()

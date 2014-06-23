class DBRouter(object):
    def db_for_read(self, model, **hints):
        if hasattr(model, 'pdns') and model.pdns:
            return 'pdns'
        return None
    def db_for_write(self, *args, **kwargs):
        return self.db_for_read(*args, **kwargs)

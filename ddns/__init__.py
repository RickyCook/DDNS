class DBRouter(object):
    def db_for_read(self, model, **hints):
        if hasattr(model, 'pdns') and model.pdns:
            return 'pdns'
        return None

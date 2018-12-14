def authentication_required(f):
    def wrapper(self, *args, **kwargs):
        if self.auth_middleware:
            if not self.auth_middleware.validate():
                print('unauthorized')
                self.set_status(403, 'unauthorized request')
                self.redirect(self.login_url)
            else:
                return f(self, *args, **kwargs)
    return wrapper
        
            
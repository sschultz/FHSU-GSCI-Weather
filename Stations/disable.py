class DisableCSRF(object):
    """
    This class disables the the use of
    Cross Site Request Forgery protection (CSRF). CSRF stops
    another server from displaying this site in a iframe. Since
    this is what we are doing with the site we have to disable
    CSRF. Normally you would disable CSRF as per view, but we
    are disabling it for the entire site with this.
    """
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

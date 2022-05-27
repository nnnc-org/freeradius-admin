from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from myapp.models import Profile

class OIDCAB(OIDCAuthenticationBackend):
    
    def get_username(self, claims):
        return unicodedata.normalize('NFKC', claims.get('email'))[:150]
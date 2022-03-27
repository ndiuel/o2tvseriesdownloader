class DownloadError(Exception):
    pass 

class SeriesNotFound(DownloadError):
    pass 


class SeasonNotFound(DownloadError):
    pass 


class EpisodeNotFound(DownloadError):
    pass 


class CaptchaLinkNotFound(DownloadError):
    pass

class DownloadLinkNotFound(DownloadError):
    pass



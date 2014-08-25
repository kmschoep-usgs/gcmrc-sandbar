from factory.django import DjangoModelFactory


class AreaVolumeCalcsFactory(DjangoModelFactory):
    FACTORY_FOR = 'surveys.AreaVolume'
    
    calc_type = 'eddy'
    
    
class SiteModelFactory(DjangoModelFactory):
    
    FACTORY_FOR = 'surveys.Site'
    

class SandbarModelFactory(DjangoModelFactory):
    
    FACTORY_FOR = 'surveys.Sandbar'
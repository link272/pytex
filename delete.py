#-*- coding : utf-8 -*-
from base import 

class DeleteBase(ModelBaseView):
    
    def remove(self, pk_pattern = "pk"):
        
        """
        Delete an object
            => pkey is needed.
                            
        Common suffix: "confirm_delete"
        
        Template exemple: "/templates/model/model_comfirm_delete"

        """
        
        try:
            objects = self.model.objects.filter(pk = pk_pattern)
            objects.delete()
            return True
        except:
            return False
    
    
                                 
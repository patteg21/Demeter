""" Space will be used for a variety of data validations and return information based 
    a given set of attributes about data.                                             """

# create functions 
class internalFunctions:
    def locationCheck(self,coordinateX,coordinateY,coordinateZ):

        if coordinateZ < 8:
            locationZ = "First Floor"
        elif coordinateZ >= 8 and coordinateZ <= 16:
            locationZ = "Second Floor"
        else:
            locationZ = "Above"
        


        pass 
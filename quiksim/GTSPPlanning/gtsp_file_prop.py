NAME = 'NAME'
TYPE = 'TYPE'
COMMENT = 'COMMENT'
DIMENSION = 'DIMENSION'
GTSP_SETS = 'GTSP_SETS'
EDGE_WEIGHT_TYPE = 'EDGE_WEIGHT_TYPE'
EDGE_WEIGHT_FORMAT = 'EDGE_WEIGHT_FORMAT'

class GTSPFileProperties:

    def __init__(self):

        # Using properties for easier usage
        # Would be nice to have explicit setters/functional generator
        self.file_name = None
        self.file_type = None
        self.comment = None
        self.dimension = None
        self.gtsp_sets = None
        self.edge_weight_type = None
        self.edge_weight_format = None

        self.init_tour_file_name = None

    def get_dict(self):

        file_properties = {
            NAME : self.file_name,
            TYPE : self.file_type,
            COMMENT : self.comment,
            DIMENSION : self.dimension,
            GTSP_SETS : self.gtsp_sets,
            EDGE_WEIGHT_TYPE : self.edge_weight_type,
            EDGE_WEIGHT_FORMAT : self.edge_weight_format
        }

        return file_properties
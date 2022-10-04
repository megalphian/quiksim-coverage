
EDGE_WEIGHT_SECTION = 'EDGE_WEIGHT_SECTION'

GTSP_SET_SECTION = 'GTSP_SET_SECTION'

END_STR = 'EOF'

class GTSPFileProperties:

    def write_to_file(self, edge_weight_matrix, gtsp_sets):
        file_name = self.gtsp_prop.file_name

        if(file_name is None):
            raise ValueError('Invalid File Name')

        gtsp_prop_dict = self.gtsp_prop.get_dict()
        
        with open((file_name + '.gtsp'), 'w') as f:
            for key, value in gtsp_prop_dict.items():
                f.write(str(key) + ': ' + str(value) + '\n')
            
            # Edge Weight Section
            f.write(str(EDGE_WEIGHT_SECTION) + '\n')
            for edge in edge_weight_matrix:
                row = ''
                for weight in edge:
                    row += '%5i '%round(weight*100)
                f.write(row + '\n')

            # GTSP Set Section
            set_counter = 1

            f.write(str(GTSP_SET_SECTION) + '\n')
            for set in gtsp_sets:
                row = str(set_counter) + ' '
                for vertex in set:
                    row += str(vertex) + ' '
                row += '-1 '
                f.write(row + '\n')

                set_counter += 1
            
            # End file
            f.write(END_STR)
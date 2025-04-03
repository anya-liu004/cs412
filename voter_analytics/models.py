from django.db import models

# Create your models here.
class Voter(models.Model):
    '''
    Store/represent the data from one registered voter in the town of Newton, MA.
    *    Last Name
    *    First Name
    *    Residential Address - Street Number
    *    Residential Address - Street Name
    *    Residential Address - Apartment Number
    *    Residential Address - Zip Code
    *    Date of Birth
    *    Date of Registration
    *    Party Affiliation (**note, this is a 2-character wide field**)
    *    Precinct Number
    These fields indicate whether or not a given voter participated in several recent elections:
    *    v20state
    *    v21town
    *    v21primary
    *    v22general
    *    v23town
    '''
    # identification
    id_number = models.TextField() 
    # bib = models.IntegerField()
    first_name = models.TextField()
    last_name = models.TextField()
    address_street_number = models.TextField()
    address_street_name = models.TextField()
    address_apartment_number = models.TextField()
    address_zip_code = models.TextField()
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2, blank=True, null=True)
    precinct_number = models.TextField()
    
    # election participation
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    # voter participation over past 5 elections
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name} ({self.address_street_number}, {self.address_street_name}), {self.date_of_birth}'
    
def string_to_bool(s):
    '''Convert a string to a boolean value.'''
    if s == 'TRUE':
        return True
    elif s == 'FALSE':
        return False
    else:
        raise ValueError(f'Invalid string for boolean conversion: {s}')

def load_data():
    '''Function to load data records from CSV file into Django model instances.'''

    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()

    filename = '/Users/anya/Downloads/newton_voters.csv'
    f = open(filename, 'r')
    f.readline() # discard headers

    for line in f:
        try:
            fields = line.strip().split(',')
            # show which value in each field
                    
            # create a new instance of Result object with this record from CSV
            result = Voter( id_number=fields[0],
                            first_name=fields[1],
                            last_name=fields[2],

                            address_street_number = fields[3],
                            address_street_name = fields[4],
                            address_apartment_number = fields[5],
                            address_zip_code = fields[6],

                            date_of_birth = fields[7],
                            date_of_registration = fields[8],

                            party_affiliation = fields[9],
                            precinct_number = fields[10],
                        
                            v20state = string_to_bool(fields[11]),
                            v21town = string_to_bool(fields[12]),
                            v21primary = string_to_bool(fields[13]),
                            v22general = string_to_bool(fields[14]),
                            v23town = string_to_bool(fields[15]),
                            voter_score = fields[16]
                        )
            result.save() # commit to database
            print(f'Created voter: {result}')
        except Exception as e:
            print(f"Skipped: {fields}")
            print(f'Error: {e}')

    print(f'Done. Created {len(Voter.objects.all())} Results.')
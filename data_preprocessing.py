
# Data Pre-Processing Steps for Dashboard


import pandas as pd

def preprocess_data(df): # This function will wrap all the pre-processing steps below to reuse for main visualization dashboard code

    df = df.dropna() # We will drop any NaNs for efficiency

    df = df.drop(columns=['Census Units', 'Total Assisted Units']) # We will drop unecessary columns for our analysis

    # To simplify analysis and reduce clutter, we divided CT's 169 towns into their respective counties
    
    county = {
        'Fairfield County': ['Bethel', 'Bridgeport', 'Brookfield', 'Danbury', 'Darien', 'Easton', 'Fairfield', 'Greenwich', 'Monroe', 
                         'New Canaan', 'New Fairfield', 'Newtown', 'Norwalk', 'Redding', 'Ridgefield', 'Shelton', 'Sherman', 'Stamford', 
                         'Stratford', 'Trumbull', 'Weston', 'Westport', 'Wilton'],
        'Hartford County': ['Avon', 'Berlin', 'Bloomfield', 'Bristol', 'Burlington', 'Canton', 'East Granby', 'East Hartford', 'East Windsor', 
                        'Enfield', 'Farmington', 'Glastonbury', 'Granby', 'Hartford', 'Hartland', 'Manchester', 'Marlborough', 'New Britain', 
                        'Newington', 'Plainville', 'Rocky Hill', 'Simsbury', 'Southington', 'South Windsor', 'Suffield', 'West Hartford', 
                        'Wethersfield', 'Windsor', 'Windsor Locks'],
        'Litchfield County': ['Barkhamsted', 'Bethlehem', 'Bridgewater', 'Canaan', 'Colebrook', 'Cornwall', 'Goshen', 'Harwinton', 'Kent', 
                          'Litchfield', 'Morris', 'New Hartford', 'New Milford', 'Norfolk', 'North Canaan', 'Plymouth', 'Roxbury', 'Salisbury', 
                          'Sharon', 'Thomaston', 'Torrington', 'Warren', 'Washington', 'Watertown', 'Winchester', 'Woodbury'],
        'Middlesex County': ['Chester', 'Clinton', 'Cromwell', 'Deep River', 'Durham', 'East Haddam', 'East Hampton', 'Essex', 'Haddam', 
                         'Killingworth', 'Middlefield', 'Middletown', 'Old Saybrook', 'Portland', 'Westbrook'],
        'New Haven County': ['Ansonia', 'Beacon Falls', 'Bethany', 'Branford', 'Cheshire', 'Derby', 'East Haven', 'Guilford', 'Hamden', 
                         'Madison', 'Meriden', 'Middlebury', 'Milford', 'Naugatuck', 'New Haven', 'North Branford', 'North Haven', 
                         'Orange', 'Oxford', 'Prospect', 'Seymour', 'Southbury', 'Wallingford', 'Waterbury', 'West Haven', 'Wolcott', 
                         'Woodbridge'],
        'New London County': ['Bozrah', 'Colchester', 'East Lyme', 'Franklin', 'Griswold', 'Groton', 'Lebanon', 'Ledyard', 'Lisbon', 
                          'Lyme', 'Montville', 'New London', 'North Stonington', 'Norwich', 'Old Lyme', 'Preston', 'Salem', 'Sprague', 
                          'Stonington', 'Voluntown', 'Waterford'],
        'Tolland County': ['Andover', 'Bolton', 'Columbia', 'Coventry', 'Ellington', 'Hebron', 'Mansfield', 'Somers', 'Stafford', 
                       'Tolland', 'Union', 'Vernon', 'Willington'],
        'Windham County': ['Ashford', 'Brooklyn', 'Canterbury', 'Chaplin', 'Eastford', 'Hampton', 'Killingly', 'Plainfield', 'Pomfret', 
                       'Putnam', 'Scotland', 'Sterling', 'Thompson', 'Windham', 'Woodstock']
    }

    # This function below will properly categorize towns into their counties based on dictionary above

    def assign_county(town):
        for county_name, towns in county.items():
            if town in towns:
                return county_name
        return None

    # County column is now added to DataFrame
    
    df['County'] = df['Town'].apply(assign_county)

    return df

                 

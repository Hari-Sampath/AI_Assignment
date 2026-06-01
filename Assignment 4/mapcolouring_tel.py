# Telangana districts
region_list = [
    "Adilabad", "Komaram Bheem", "Mancherial", "Nirmal", "Nizamabad",
    "Jagitial", "Peddapalli", "Karimnagar", "Rajanna Sircilla", "Kamareddy",
    "Sangareddy", "Medak", "Siddipet", "Jangaon", "Yadadri",
    "Hyderabad", "Medchal", "Rangareddy", "Vikarabad",
    "Mahabubnagar", "Narayanpet", "Wanaparthy", "Nagarkurnool", "Jogulamba Gadwal",
    "Nalgonda", "Suryapet", "Khammam", "Bhadradri Kothagudem",
    "Mulugu", "Mahabubabad", "Jayashankar", "Warangal Rural", "Hanamkonda"
]

available_colors = ["Red", "Green", "Blue", "Yellow"]

# Adjacency information
adjacent_districts = {
    "Adilabad": ["Nirmal", "Komaram Bheem", "Mancherial"],
    "Komaram Bheem": ["Adilabad", "Mancherial"],
    "Mancherial": ["Komaram Bheem", "Peddapalli", "Jayashankar", "Adilabad"],
    "Nirmal": ["Adilabad", "Nizamabad", "Jagitial"],
    "Nizamabad": ["Nirmal", "Kamareddy", "Jagitial"],
    "Kamareddy": ["Nizamabad", "Medak", "Siddipet"],

    "Jagitial": ["Nirmal", "Karimnagar", "Peddapalli", "Rajanna Sircilla", "Nizamabad"],
    "Peddapalli": ["Jagitial", "Karimnagar", "Mancherial"],
    "Karimnagar": ["Jagitial", "Peddapalli", "Rajanna Sircilla", "Siddipet"],
    "Rajanna Sircilla": ["Karimnagar", "Siddipet", "Jagitial"],

    "Medak": ["Kamareddy", "Sangareddy", "Siddipet"],
    "Sangareddy": ["Medak", "Vikarabad", "Rangareddy"],
    "Siddipet": ["Medak", "Rajanna Sircilla", "Karimnagar", "Jangaon", "Kamareddy"],

    "Jangaon": ["Siddipet", "Warangal Rural", "Yadadri", "Hanamkonda"],
    "Yadadri": ["Jangaon", "Nalgonda", "Rangareddy", "Suryapet"],

    "Hyderabad": ["Rangareddy", "Medchal"],
    "Medchal": ["Hyderabad", "Rangareddy"],
    "Rangareddy": ["Hyderabad", "Medchal", "Vikarabad", "Yadadri", "Mahabubnagar"],
    "Vikarabad": ["Sangareddy", "Rangareddy"],

    "Mahabubnagar": ["Narayanpet", "Wanaparthy", "Rangareddy"],
    "Narayanpet": ["Mahabubnagar", "Jogulamba Gadwal"],
    "Wanaparthy": ["Mahabubnagar", "Nagarkurnool"],
    "Nagarkurnool": ["Wanaparthy", "Nalgonda"],
    "Jogulamba Gadwal": ["Narayanpet", "Mahabubnagar"],

    "Nalgonda": ["Yadadri", "Suryapet", "Nagarkurnool"],
    "Suryapet": ["Nalgonda", "Khammam", "Yadadri"],
    "Khammam": ["Suryapet", "Bhadradri Kothagudem", "Mahabubabad"],
    "Bhadradri Kothagudem": ["Khammam", "Mulugu"],

    "Mulugu": ["Bhadradri Kothagudem", "Jayashankar"],
    "Jayashankar": ["Mulugu", "Mancherial", "Warangal Rural"],

    "Mahabubabad": ["Warangal Rural", "Khammam"],
    "Warangal Rural": ["Jangaon", "Mahabubabad", "Hanamkonda", "Jayashankar"],
    "Hanamkonda": ["Warangal Rural", "Jangaon"]
}

# Function to verify whether a chosen color can be assigned
def can_assign(region, shade, assignment_map):
    nearby = adjacent_districts.get(region, [])
    for border_region in nearby:
        if border_region in assignment_map and assignment_map[border_region] == shade:
            return False
    return True

# Recursive coloring function
def color_telangana(assignment_map):
    if len(assignment_map) == len(region_list):
        return True

    uncolored = None
    for region in region_list:
        if region not in assignment_map:
            uncolored = region
            break

    for shade in available_colors:
        if can_assign(uncolored, shade, assignment_map):
            assignment_map[uncolored] = shade

            if color_telangana(assignment_map):
                return True

            del assignment_map[uncolored]

    return False

final_coloring = {}
color_telangana(final_coloring)

print("\nColor Assignment for Telangana Districts:\n")
for region in region_list:
    print(f"{region:25} : {final_coloring[region]}")

print("\nValidation Report:\n")
issue_found = False
for region, nearby_list in adjacent_districts.items():
    for border_region in nearby_list:
        if final_coloring[region] == final_coloring[border_region]:
            print(f"Conflict detected between {region} and {border_region}")
            issue_found = True

if not issue_found:
    print("No coloring conflicts found.")
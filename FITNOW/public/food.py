import requests

img = 'test.jpg'
api_user_token = '985b9e806fdf35d70b6334a58e0ce7cdf176903e'
headers = {'Authorization': 'Bearer ' + api_user_token}

# Single/Several Dishes Detection
url = 'https://api.logmeal.com/v2/image/segmentation/complete'
resp = requests.post(url, files={'image': open(img, 'rb')}, headers=headers)

# Check if the response contains 'imageId'
if 'imageId' in resp.json():
    image_id = resp.json()['imageId']
    
    # Nutritional information
    url = 'https://api.logmeal.com/v2/recipe/nutritionalInfo'
    resp = requests.post(url, json={'imageId': image_id}, headers=headers)
    nutritional_info = resp.json()

    # Filter for specific percent categories and get only the level
    required_categories = ['FAT', 'SUGAR', 'PROCNT', 'CHOCDF']

    # Initialize variables
    fatLevel = sugarLevel = proteinLevel = carbLevel = None

    # Extract levels
    for category in required_categories:
        if category in nutritional_info['nutritional_info']['dailyIntakeReference']:
            category_info = nutritional_info['nutritional_info']['dailyIntakeReference'][category]
            if category == 'FAT':
                fatLevel = category_info['level']
            elif category == 'SUGAR':
                sugarLevel = category_info['level']
            elif category == 'PROCNT':
                proteinLevel = category_info['level']
            elif category == 'CHOCDF':
                carbLevel = category_info['level']

    print("Fat Level:", fatLevel)
    print("Sugar Level:", sugarLevel)
    print("Protein Level:", proteinLevel)
    print("Carb Level:", carbLevel)

    def grade_meal(carbLevel, proteinLevel, fatLevel, sugarLevel):
        score = 0
        
        # Evaluate carbohydrate level
        if carbLevel == "HIGH":
            score += 1
        elif carbLevel == "MEDIUM":
            score += 0
        elif carbLevel == "LOW":
            score += 1
        else:
            score += 2
        
        # Evaluate protein level
        if proteinLevel == "HIGH":
            score += 0
        elif proteinLevel == "MEDIUM":
            score += 0
        elif proteinLevel == "LOW":
            score += 1
        else:
            score += 2
        
        # Evaluate fat level
        if fatLevel == "HIGH":
            score += 3
        elif fatLevel == "MEDIUM":
            score += 2
        elif fatLevel == "LOW":
            score += 1
        else:
            score += 2
        
        # Evaluate sugar level
        if sugarLevel == "HIGH":
            score += 3
        elif sugarLevel == "MEDIUM":
            score += 2
        elif sugarLevel == "LOW":
            score += 1
        else:
            score += 0

        # Determine grade based on score
        if score <= 1:
            return "A"
        elif score <= 3:
            return "B"
        elif score <= 5:
            return "C"
        else:
            return "D"

    grade = grade_meal(carbLevel, proteinLevel, fatLevel, sugarLevel)
    print(f"The meal is graded: {grade}")

else:
    print("Error: 'imageId' not found in the response from the segmentation API.")

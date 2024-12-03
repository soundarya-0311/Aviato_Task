import json

data = {
  "employee": {
    "id": 12345,
    "name": "John Doe",
    "contact": {
      "email": "john.doe@example.com",
      "phone": "123-456-7890"
    },
    "projects": [
      {
        "project_id": 1,
        "name": "Project Alpha",
        "details": {
          "start_date": "2023-01-15",
          "end_date": "2023-07-30",
          "team_members": [
            {"id": 101, "name": "Alice Smith", "role": "Developer"},
            {"id": 102, "name": "Bob Johnson", "role": "Tester"}
          ]
        }
      },
      {
        "project_id": 2,
        "name": "Project Beta",
        "details": {
          "start_date": "2023-08-01",
          "end_date": "2023-12-31",
          "team_members": [
            {"id": 103, "name": "Charlie Lee", "role": "Designer"},
            {"id": 104, "name": "David Kim", "role": "Product Manager"}
          ]
        }
      }
    ]
  }
}

employee_info = {
    "employee_id": data["employee"]["id"],
    "employee_name": data["employee"]["name"],
    "contact_email": data["employee"]["contact"]["email"],
    "contact_phone": data["employee"]["contact"]["phone"]
}

employee_projects = [
    {**employee_info,  
     "project_id": project["project_id"],
     "project_name": project["name"],
     "project_start_date": project["details"]["start_date"],
     "project_end_date": project["details"]["end_date"],
     "team_members": [
         {"team_member_id": member["id"], "team_member_name": member["name"], "role": member["role"]}
         for member in project["details"]["team_members"]
     ]}
    for project in data["employee"]["projects"]
]

print(json.dumps(employee_projects, indent=2))

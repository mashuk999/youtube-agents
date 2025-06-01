import json

def get_object_by_index(json_file='data.json', index_file='currentindex.txt'):
    try:
        # Read the index
        with open(index_file, 'r') as f:
            index = int(f.read().strip())

        # Read the JSON data
        with open(json_file, 'r') as f:
            data = json.load(f)

        # Return the object at the index
        return data[index-1]['name']
    
    except FileNotFoundError as e:
        return f"Error: File not found - {e.filename}"
    except ValueError:
        return "Error: Invalid index format in currentindex.txt"
    except IndexError:
        return "Error: Index out of range in data.json"
    except json.JSONDecodeError:
        return "Error: Failed to parse JSON data"
import requests

# current_index_name = '.kibana_1'
# new_index_name = 'kibana'
# base_url = 'https://search-vacationplanner-pu2vusfddg2zccevu5vwkzr74y.ap-south-1.es.amazonaws.com'
# mapping_changes = {
#     "type": {"type": "keyword"}
# }

# ------------------------------------------------
# Get current mapping
def display_current_mapping(base_url, old_index, changed_mapping):
    r = requests.get('{base_url}/{index_name}'.format(base_url=base_url, index_name=old_index))
    r.raise_for_status()
    content = r.json()
    mappings = content[old_index]['mappings']
    mappings['properties'].update(changed_mapping)
    return mappings

# ------------------------------------------------
# Create a new index with the correct mappings
def create_index(base_url, new_index, mappings):
    r = requests.put('{base_url}/{index_name}'.format(base_url=base_url, index_name=new_index), json={
        'mappings': mappings
    })
    r.raise_for_status()
    return

# ------------------------------------------------
# Reindex
def perform_reindex(base_url, old_index, new_index):
    r = requests.post('{base_url}/_reindex'.format(base_url=base_url), json={
        "source": {
            "index": old_index
        },
        "dest": {
            "index": new_index
        }
    })
    r.raise_for_status()
    return

# ------------------------------------------------
# Delete the old index
def delete_index(base_url, old_index):
    r = requests.delete('{base_url}/{index_name}'.format(base_url=base_url, index_name=old_index))
    r.raise_for_status()
    return

# ------------------------------------------------
# Create an alias (so that on next time this will be easier to do without downtime)
def create_alias(base_url, new_index, old_index):
    r = requests.post('{base_url}/_aliases'.format(base_url=base_url), json={
        "actions": [
            {"add": {
                "alias": old_index,
                "index": new_index
            }}
        ]
    })
    r.raise_for_status()
    return


if __name__ == "__main__":
    current_index_name = 'aviasales'
    #new_index_name = '.kibana'
    base_url = 'https://search-vacationplanner-pu2vusfddg2zccevu5vwkzr74y.ap-south-1.es.amazonaws.com'
    # mapping_changes = {
    #     "type": {"type": "keyword"}
    # }
    #
    # mappings = display_current_mapping(base_url, current_index_name, mapping_changes)
    # create_index(base_url, new_index_name, mappings)
    # perform_reindex(base_url, current_index_name, new_index_name)
    delete_index(base_url, current_index_name)

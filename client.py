import argparse
import zipfile
from sword2 import Connection
from sword2 import Entry

parser = argparse.ArgumentParser(description='Upload a folder as a zipfile into a sword repository.')
parser.add_argument('-u',
                    dest='user',
                    action='store',
                    default='',
                    help='The username for authentication with the sword server.')

parser.add_argument('-p',
                    dest='password',
                    action='store',
                    default='',
                    help='The password for authentication with the sword server.')

parser.add_argument('-s',
                    dest='sd_uri',
                    action='store',
                    default='',
                    help='The URI of the service document for the repository.')

sword_args = parser.parse_args()

sd_uri = sword_args.sd_uri
user = sword_args.user
password = sword_args.password

connection = Connection(sd_uri, user_name=user, user_pass=password)


connection.get_service_document()

# If we have no workspaces, exit with a sensible message.
if not connection.workspaces:
    print 'There are no available workspaces to upload to. You might need to set a username and password'
    sys.exit()

# If there is only one workspace, use it.
if len(connection.workspaces) == 1:
    workspace_title, workspace_collections = connection.workspaces[0]
else:
    # Give the user a choice of workspaces.
    print 'Please type the number of the workspace you want to upload to:'
    for i in range(len(connection.workspaces)-1):
        print '%s: %s' % (i+1, connection.workspaces[i])
    workspace_index = int(raw_input())
    workspace_title, workspace_collections = connection.workspaces[
                                                 workspace_index - 1]

# If we have no collections, exit with a sensible message.
if not workspace_collections:
    print 'There are no available collections to upload to. You might need to set a username and password'
    sys.exit()

# If there is only one collection, use it.
if len(workspace_collections) == 1:
    collection = workspace_collections[0]
else:
    # Give the user a choice of collections.
    print 'Please type the number of the collection you want to upload to:'
    for i in range(len(workspace_collections)-1):
        print '%s: %s' % (i+1, workspace_collections[i].title)
    collection_index = int(raw_input())
    collection = workspace_collections[collection_index - 1]


# Add a metadata record to this newly created resource (or 'container')
# Entry can be passed keyword parameters to add metadata to the entry (namespace + '_' + tagname)
entry = Entry(id="atomid", 
          title="atom-title",
          dcterms_abstract = "Info about the resource....")
# upload "package.zip" to this collection as a new (binary) resource:
with open("package.zip", "r") as pkg:
    receipt = connection.create(col_iri = collection.href,
                                payload = pkg,
                                mimetype = "application/zip",
                                filename = "package.zip",
                                packaging = 'http://purl.org/net/sword/package/Binary',
                                metadata_entry=entry,
                                in_progress = True)    # As the deposit isn't yet finished


# Update the metadata entry to the resource:
updated_receipt = connection.update(metadata_entry = entry,
                           dr = receipt,   # use the receipt to discover the right URI to use
                           in_progress = False)  # finish the deposit



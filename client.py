import argparse
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
import pdb;pdb.set_trace()
# pick the first collection within the first workspace:
workspace_1_title, workspace_1_collections = connection.workspaces[0]
collection = workspace_1_collections[0]

# upload "package.zip" to this collection as a new (binary) resource:
with open("package.zip", "r") as pkg:
    receipt = connection.create(col_iri = collection.href,
                                payload = pkg,
                                mimetype = "application/zip",
                                filename = "package.zip",
                                packaging = 'http://purl.org/net/sword/package/Binary',
                                in_progress = True)    # As the deposit isn't yet finished


# Add a metadata record to this newly created resource (or 'container')
# Entry can be passed keyword parameters to add metadata to the entry (namespace + '_' + tagname)
entry = Entry(id="atomid", 
          title="atom-title",
          dcterms_abstract = "Info about the resource....")
# to add a new namespace:
entry.register_namespace('skos', 'http://www.w3.org/2004/02/skos/core#')
entry.add_field("skos_Concept", "...")


# Update the metadata entry to the resource:
updated_receipt = connection.update(metadata_entry = entry,
                           dr = receipt,   # use the receipt to discover the right URI to use
                           in_progress = False)  # finish the deposit



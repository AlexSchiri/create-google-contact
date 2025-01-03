import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from optparse import OptionParser
import sys


# PERMESSI
SCOPES = ["https://www.googleapis.com/auth/contacts.readonly",
          "https://www.googleapis.com/auth/contacts"]


def main():

  parser = OptionParser()
  parser.add_option('-n','--name',dest = 'name',
                    help='name')
  parser.add_option('-p','--phone',dest = 'phone',
                    help='phone')
  parser.add_option('-e','--email',dest = 'email',
                    help='email')
  parser.add_option('-c','--codcli',dest = 'codcli',
                    help='codcli')
  
  (options,args) = parser.parse_args()

  """Shows basic usage of the People API.
  """
  creds = None
  found = False
  #file token.json creato automaticamente la prima volta, contiene gli accessi
  #dell'utente
  if os.path.exists(r"C:\Users\ALESSANDRO\Documents\dist\create_contact_google\token.json"):
    creds = Credentials.from_authorized_user_file(r"C:\Users\ALESSANDRO\Documents\dist\create_contact_google\token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          r"C:\Users\ALESSANDRO\Documents\dist\create_contact_google\credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=8080)
    #Salva le credenziali per la prossima volta
    with open(r"C:\Users\ALESSANDRO\Documents\dist\create_contact_google\token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("people", "v1", credentials=creds)

    # Call the People API
    results = (
        service.people()
        .connections()
        .list(
            resourceName="people/me",
            pageSize=10,
            personFields="names,emailAddresses,phoneNumbers",
        )
        .execute()
    )
    connections = results.get("connections", [])
    person_names = [person.get("names",[]) for person in connections]
    person_emails = [person.get("emailAddresses",[]) for person in connections]
    person_phones = [person.get("phoneNumbers",[]) for person in connections]

    #recupero tutti i contatti
    names = [x[0].get("displayName") for x in person_names if x]
    emails = [y[0].get("value") for y in person_emails if y]
    phones = [z[0].get("value") for z in person_phones if z]

    #verifico se il contatto già esiste
    #se esiste non creo nulla
    for email in emails:
      if found == True:
        break
      if email == options.email:
        found = True    

    if found == False:
      for phone in phones:
        if found == True:
          break
        if phone == options.phone:
          found = True


    if options.phone and options.email and found == False:
      service.people().createContact(body={"names": [{"givenName": str(options.name) + ' - ' + str(options.codcli)}],
                                           "phoneNumbers": [{'value': str(options.phone)}],
                                           "emailAddresses": [{'value': str(options.email)}],
                                           }).execute()


  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()

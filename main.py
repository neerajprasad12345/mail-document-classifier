import argparse
from gmailapi import GmailApi


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--creds", default=None, help="Path to the credentials file.")

    args = parser.parse_args()

    gmail_api = GmailApi(args.creds)
    labels = gmail_api.get_labels()

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])


if __name__ == '__main__':
    main()
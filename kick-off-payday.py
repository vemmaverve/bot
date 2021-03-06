#!/usr/bin/env python3
import os, sys; sys.path.insert(0, os.path.dirname(__file__))

import re
import botlib


class Paydays(botlib.Issues):

    def find_previous(self):
        return self.hit_api('get', params={'state': 'all', 'labels': 'Payday'})[0]

    def create_next(self, previous):
        prev_title = previous['title']
        assert re.match(r"run Gratipay [0-9]+", prev_title), prev_title

        prev_payday_number = prev_title.split()[-1]

        prev_ticket_number = previous['number']
        assert type(prev_ticket_number) is int, prev_ticket_number

        prev_link = '[&larr; Payday {}]({}/{})'
        prev_link = prev_link.format(prev_payday_number, self.urls['html'], previous['number'])

        n = int(prev_title.split()[-1])
        next_title = 'run Gratipay {}'.format(n + 1)
        next_body = [prev_link] + previous['body'].splitlines()[1:]
        next_body = '\n'.join(next_body).strip()

        payload = {'title': next_title, 'body': next_body, 'labels': ['Payday']}
        ticket = self.hit_api('post', json=payload)
        print("created {}".format(ticket['html_url']))


@botlib.main
def main(repo, username, password):
    paydays = Paydays(repo, username, password)
    previous = paydays.find_previous()
    paydays.create_next(previous)


if __name__ == '__main__':
    main()

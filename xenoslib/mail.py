#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import email
import datetime
from time import sleep
import logging
from collections import deque

from imapclient import IMAPClient


logger = logging.getLogger(__name__)


class MailFetcher:
    """
    keep fetching from mail inbox using IMAP protocol
    usage:

    for mail in MailFetcher(imap_server, mail_addr, mail_pwd, interval=30, days=1):
        print(mail)
    """

    msg_ids = deque(maxlen=999)

    def __new__(cls, imap_server, mail_addr, mail_pwd, interval=30, days=1):
        self = super().__new__(cls)
        self.imap_server = imap_server
        self.mail_addr = mail_addr
        self.mail_pwd = mail_pwd
        self.days = days
        return self.fetching(interval=interval)

    def fetching(self, interval=30):
        """keep fetching every interval"""
        logger.debug("start checking mails...")
        while True:
            try:
                yield from self.mail_parse_generator(self.fetch_mails())
            except Exception as exc:
                logger.warning(exc)
            sleep(interval)

    def mail_parse_generator(self, mails):
        for msg_id, msg in mails.items():
            if msg_id in self.msg_ids:
                continue
            body = email.message_from_bytes(msg[b"BODY[]"])
            subject = str(email.header.make_header(email.header.decode_header(body["Subject"])))
            from_ = body["From"]
            date = body["Date"]
            payload = body.get_payload(decode=True)
            if payload:
                payload = payload.decode()
            internal_date = msg[b"INTERNALDATE"]
            msg = {
                "body": body,
                "subject": subject,
                "payload": payload,
                "date": date,
                "from": from_,
                "internal_date": internal_date,
            }
            yield msg
            self.msg_ids.append(msg_id)

    def fetch_mails(self):
        """login and fetch mails once"""
        logger.debug(f"fetching mails in {self.days} day(s)...")
        date_str = datetime.datetime.today() - datetime.timedelta(days=self.days)
        with IMAPClient(self.imap_server, timeout=30) as client:
            client.login(self.mail_addr, self.mail_pwd)
            client.select_folder("INBOX", readonly=True)
            messages = client.search(["SINCE", date_str])
            mails = client.fetch(messages, ["INTERNALDATE", "BODY.PEEK[]"])
            return mails


def test():
    try:
        import env  # noqa
    except ModuleNotFoundError:
        pass
    imap_server = os.environ["imap_server"]
    mail_addr = os.environ["imap_addr"]
    mail_pwd = os.environ["imap_pass"]
    for mail in MailFetcher(imap_server, mail_addr, mail_pwd, interval=1, days=33):
        print(mail["subject"])


if __name__ == "__main__":
    test()

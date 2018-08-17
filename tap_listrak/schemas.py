#!/usr/bin/env python3
import os
import singer
from singer import utils


class IDS(object):
    LISTS = "lists"
    MESSAGES = "messages"
    MESSAGE_CLICKS = "message_clicks"
    MESSAGE_OPENS = "message_opens"
    MESSAGE_READS = "message_reads"
    MESSAGE_SENDS = "message_sends"
    MESSAGE_UNSUBS = "message_unsubs"
    MESSAGE_BOUNCES = "message_bounces"
    SUBSCRIBED_CONTACTS = "subscribed_contacts"

stream_ids = [getattr(IDS, x) for x in dir(IDS)
              if not x.startswith("__")]

PK_FIELDS = {
    IDS.LISTS: ["ListID"],
    IDS.MESSAGES: ["MsgID"],
    IDS.MESSAGE_CLICKS: ["MsgID", "EmailAddress"],
    IDS.MESSAGE_OPENS: ["MsgID", "EmailAddress"],
    IDS.MESSAGE_READS: ["MsgID", "EmailAddress"],
    IDS.MESSAGE_SENDS: ["MsgID", "EmailAddress"],
    IDS.MESSAGE_UNSUBS: ["MsgID", "EmailAddress"],
    IDS.MESSAGE_BOUNCES: ["MsgID", "EmailAddress"],
    IDS.SUBSCRIBED_CONTACTS: ["ListID", "ContactID"],
}


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def get_stream_from_catalog(stream_id, catalog):
    streams = catalog['streams']
    for s in streams:
        if s['tap_stream_id'] == stream_id:
            return s


def load_and_write_schema(tap_stream_id, catalog):
    stream = get_stream_from_catalog(tap_stream_id, catalog)
    singer.write_schema(
        tap_stream_id, stream['schema'], PK_FIELDS[tap_stream_id])

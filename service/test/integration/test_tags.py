#
# Copyright (c) 2014 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
import json

from test.support.integration import *
from pixelated.adapter.services.tag_service import TagService


class TagsTest(SoledadTestBase):

    def setUp(self):
        SoledadTestBase.setUp(self)

    def tearDown(self):
        SoledadTestBase.tearDown(self)

    def _tags_json(self, tags):
        return json.dumps({'newtags': tags})

    def test_add_tag_to_an_inbox_mail_and_query(self):
        mail = MailBuilder().with_subject('Mail with tags').build_input_mail()
        self.client.add_mail_to_inbox(mail)

        self.post_tags(mail.ident, self._tags_json(['IMPORTANT']))

        mails = self.get_mails_by_tag('inbox')
        self.assertEquals({'important'}, set(mails[0].tags))

        mails = self.get_mails_by_tag('important')
        self.assertEquals('Mail with tags', mails[0].subject)

    def test_empty_tags_are_not_allowed(self):
        mail = MailBuilder().with_subject('Mail with tags').build_input_mail()
        self.client.add_mail_to_inbox(mail)

        self.post_tags(mail.ident, self._tags_json(['tag1', '   ']))

        mail = self.get_mail(mail.ident)

        self.assertEquals(mail['tags'], ['tag1'])

    def test_addition_of_reserved_tags_is_not_allowed(self):
        mail = MailBuilder().with_subject('Mail with tags').build_input_mail()
        self.client.add_mail_to_inbox(mail)

        for tag in TagService.SPECIAL_TAGS:
            response = self.post_tags(mail.ident, self._tags_json([tag.name.upper()]))
            self.assertEquals("None of the following words can be used as tags: %s" % tag.name, response)

        mail = self.client.mailboxes.inbox().mail(mail.ident)
        self.assertNotIn('drafts', mail.tags)
